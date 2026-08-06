"""
Report generation endpoints – no authentication required.
"""

import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.database import get_db
from app.models.agent_log import AgentLog
from app.models.report import Report
from app.models.user import User
from app.schemas.report import EmailReportRequest, ReportGenerateRequest, ReportResponse

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    payload: ReportGenerateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from services.report_service import generate_report_pdf

    log_result = await db.execute(
        select(AgentLog)
        .where(
            AgentLog.user_id == current_user.id,
            AgentLog.session_id == payload.session_id,
            AgentLog.status == "success",
        )
        .order_by(AgentLog.created_at)
    )
    logs = log_result.scalars().all()

    if not logs:
        raise HTTPException(status_code=404, detail="No completed agent session found. Run agents first.")

    content: dict = {}
    for log in logs:
        content[log.agent_name] = log.output_data

    report_id = uuid.uuid4()
    report = Report(
        id=report_id,
        user_id=current_user.id,
        session_id=payload.session_id,
        report_type=payload.report_type,
        title=f"EduPilot Study Abroad Report – {current_user.full_name}",
        summary="Personalised AI-generated study abroad recommendation report.",
        content=content,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    background_tasks.add_task(
        generate_report_pdf,
        report_id=str(report_id),
        user_name=current_user.full_name,
        content=content,
    )

    if payload.send_email and payload.email_recipient:
        background_tasks.add_task(
            _send_report_email,
            report_id=str(report_id),
            recipient=str(payload.email_recipient),
            user_name=current_user.full_name,
        )

    return ReportResponse(
        id=str(report.id),
        session_id=report.session_id,
        report_type=report.report_type,
        title=report.title,
        summary=report.summary,
        content=report.content,
        pdf_path=report.pdf_path,
        email_sent=report.email_sent,
        created_at=report.created_at.isoformat(),
    )


@router.get("", response_model=list[ReportResponse])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Report)
        .where(Report.user_id == current_user.id)
        .order_by(Report.created_at.desc())
        .limit(20)
    )
    reports = result.scalars().all()
    return [
        ReportResponse(
            id=str(r.id),
            session_id=r.session_id,
            report_type=r.report_type,
            title=r.title,
            summary=r.summary,
            content=r.content,
            pdf_path=r.pdf_path,
            email_sent=r.email_sent,
            created_at=r.created_at.isoformat(),
        )
        for r in reports
    ]


@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.pdf_path or not Path(report.pdf_path).exists():
        raise HTTPException(status_code=404, detail="PDF not ready yet. Try again shortly.")
    return FileResponse(
        path=report.pdf_path,
        media_type="application/pdf",
        filename=f"edupilot_report_{report_id[:8]}.pdf",
    )


@router.post("/email")
async def email_report(
    payload: EmailReportRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(Report).where(Report.id == payload.report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    background_tasks.add_task(
        _send_report_email,
        report_id=payload.report_id,
        recipient=str(payload.recipient),
        user_name=current_user.full_name,
        subject=payload.subject,
        message=payload.message,
    )
    return {"status": "queued", "recipient": str(payload.recipient)}


async def _send_report_email(
    report_id: str,
    recipient: str,
    user_name: str,
    subject: str | None = None,
    message: str | None = None,
):
    from datetime import datetime, timezone
    from mcp_tools.gmail_mcp import GmailMCPClient
    from app.database import AsyncSessionLocal

    client = GmailMCPClient()
    success = await client.send_report_email(
        report_id=report_id,
        recipient=recipient,
        user_name=user_name,
        subject=subject,
        message=message,
    )

    if success:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Report).where(Report.id == report_id))
            report = result.scalar_one_or_none()
            if report:
                report.email_sent = True
                report.email_sent_at = datetime.now(timezone.utc)
                report.email_recipient = recipient
                await db.commit()
