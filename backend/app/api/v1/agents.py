"""
Agent execution endpoints – persistent chat sessions, auto-report generation.
"""

import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.database import get_db
from app.models.agent_log import AgentLog
from app.models.chat_session import ChatSession
from app.models.report import Report
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.agent import AgentLogResponse, AgentRunRequest, AgentRunResponse, ChatRequest

router = APIRouter(prefix="/agents", tags=["AI Agents"])


@router.post("/run", response_model=AgentRunResponse)
async def run_agents(
    payload: AgentRunRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from agents.orchestrator import run_orchestrator

    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    session_id = payload.session_id or f"session_{uuid.uuid4().hex[:12]}"
    start_time = time.time()

    try:
        agent_result = await run_orchestrator(
            query=payload.query,
            session_id=session_id,
            student_profile=profile,
            user_id=str(current_user.id),
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

    elapsed_ms = (time.time() - start_time) * 1000

    # Auto-generate report after successful run
    await _auto_create_report(
        session_id=session_id,
        user_id=current_user.id,
        user_name=current_user.full_name,
        output=agent_result.get("output", {}),
        agents_executed=agent_result.get("agents_executed", []),
        db=db,
    )

    return AgentRunResponse(
        session_id=session_id,
        status="success",
        agents_executed=agent_result.get("agents_executed", []),
        result=agent_result.get("output", {}),
        reasoning=agent_result.get("reasoning"),
        tokens_used=agent_result.get("tokens_used", 0),
        execution_time_ms=elapsed_ms,
    )


@router.post("/chat")
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from agents.orchestrator import run_orchestrator

    profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()

    # Get or create session
    session_id = payload.session_id or f"chat_{uuid.uuid4().hex[:12]}"
    session = await _get_or_create_session(session_id, current_user.id, db)

    # Use stored history from DB (not client-sent history)
    stored_messages = session.messages
    history = [
        type("Msg", (), {"role": m["role"], "content": m["content"]})()
        for m in stored_messages[-10:]  # last 10 messages as context
    ]

    agent_result = await run_orchestrator(
        query=payload.message,
        session_id=session_id,
        student_profile=profile,
        user_id=str(current_user.id),
        db=db,
        chat_history=history,
    )

    ai_content = agent_result.get("output", {}).get("message", "")
    agents_used = agent_result.get("agents_executed", [])

    # Save messages to session
    messages = list(session.messages)
    messages.append({
        "role": "user",
        "content": payload.message,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })
    messages.append({
        "role": "assistant",
        "content": ai_content,
        "agents_used": agents_used,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })
    session.messages = messages

    # Auto-title session from first user message
    if len(messages) <= 3 and session.title == "New Chat":
        session.title = payload.message[:60] + ("..." if len(payload.message) > 60 else "")

    await db.commit()

    # Auto-generate report after agent run
    await _auto_create_report(
        session_id=session_id,
        user_id=current_user.id,
        user_name=current_user.full_name,
        output=agent_result.get("output", {}),
        agents_executed=agents_used,
        db=db,
    )

    return {
        "session_id": session_id,
        "role": "assistant",
        "content": ai_content,
        "agents_used": agents_used,
    }


@router.get("/sessions")
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all chat sessions for the current user."""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .limit(20)
    )
    sessions = result.scalars().all()
    return [
        {
            "session_id": s.session_id,
            "title": s.title,
            "message_count": len(s.messages),
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat(),
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get full message history for a session."""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session.session_id,
        "title": session.title,
        "messages": session.messages,
        "created_at": session.created_at.isoformat(),
    }


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a chat session."""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session:
        await db.delete(session)
        await db.commit()
    return {"status": "deleted"}


@router.get("/logs", response_model=list[AgentLogResponse])
async def get_logs(
    session_id: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    query = select(AgentLog).where(AgentLog.user_id == current_user.id)
    if session_id:
        query = query.where(AgentLog.session_id == session_id)
    query = query.order_by(AgentLog.created_at.desc()).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    return [
        AgentLogResponse(
            id=str(log.id),
            session_id=log.session_id,
            agent_name=log.agent_name,
            action=log.action,
            status=log.status,
            reasoning=log.reasoning,
            tokens_used=log.tokens_used,
            execution_time_ms=log.execution_time_ms,
            created_at=log.created_at.isoformat(),
        )
        for log in logs
    ]


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _get_or_create_session(
    session_id: str, user_id: uuid.UUID, db: AsyncSession
) -> ChatSession:
    result = await db.execute(
        select(ChatSession).where(ChatSession.session_id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        session = ChatSession(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            messages=[],
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
    return session


async def _auto_create_report(
    session_id: str,
    user_id: uuid.UUID,
    user_name: str,
    output: dict,
    agents_executed: list,
    db: AsyncSession,
):
    """Automatically create a report record after agents run."""
    try:
        # Check if report already exists for this session
        result = await db.execute(
            select(Report).where(Report.session_id == session_id)
        )
        if result.scalar_one_or_none():
            return  # Already exists

        # Only create if meaningful results were returned
        has_content = (
            output.get("recommended_universities")
            or output.get("matched_scholarships")
            or output.get("finance_breakdown")
            or output.get("message")
        )
        if not has_content:
            return

        # Build report content from output
        content = {
            "final_report": output.get("final_report", {}),
            "recommended_universities": output.get("recommended_universities", []),
            "recommended_countries": output.get("recommended_countries", []),
            "matched_scholarships": output.get("matched_scholarships", []),
            "finance_breakdown": output.get("finance_breakdown", {}),
            "application_timeline": output.get("application_timeline", []),
        }

        report = Report(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            report_type="full",
            title=f"Study Abroad Report – {user_name}",
            summary="AI-generated study abroad recommendation report.",
            content=content,
        )
        db.add(report)
        await db.commit()

        # Generate PDF in background
        from services.report_service import generate_report_pdf
        import asyncio
        asyncio.create_task(
            generate_report_pdf(
                report_id=str(report.id),
                user_name=user_name,
                content=content,
            )
        )
    except Exception as e:
        pass  # Non-critical
