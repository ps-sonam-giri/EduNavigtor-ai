"""
Report generation endpoints and email dispatch.
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.database import get_db
from app.models.agent_log import AgentLog
from app.models.report import Report
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.report import EmailReportRequest, ReportGenerateRequest, ReportResponse
from mcp_tools.gmail_mcp import GmailMCPClient

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    payload: ReportGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from services.report_service import generate_report_pdf

    # 1. Fetch Student Profile
    profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()

    profile_dict = {}
    if profile:
        profile_dict = {
            "cgpa": profile.cgpa or 8.5,
            "cgpa_scale": profile.cgpa_scale or 10.0,
            "degree": profile.degree or "Bachelor of Technology",
            "specialization": profile.specialization or "Computer Science & Engineering",
            "ielts_score": profile.ielts_score or 7.5,
            "gre_score": profile.gre_score or 320,
            "total_budget_usd": profile.total_budget_usd or 35000,
            "preferred_countries": profile.preferred_countries or ["Germany", "USA", "UK"],
            "target_intake": profile.target_intake or "Fall 2026",
            "course_interest": profile.course_interest or "Master in Computer Science",
        }

    # 2. Fetch Agent Logs
    log_result = await db.execute(
        select(AgentLog)
        .where(AgentLog.user_id == current_user.id)
        .order_by(AgentLog.created_at.desc())
        .limit(20)
    )
    logs = log_result.scalars().all()

    content: dict = {"student_profile": profile_dict}
    for log in logs:
        if isinstance(log.output_data, dict):
            content.update(log.output_data)
        elif log.output_data:
            content[log.agent_name] = log.output_data

    # 3. Create DB Report record
    report_id = uuid.uuid4()
    report = Report(
        id=report_id,
        user_id=current_user.id,
        session_id=payload.session_id or "default_session",
        report_type=payload.report_type,
        title=f"EduPilot Study Abroad Report – {current_user.full_name}",
        summary="Personalised AI-generated study abroad recommendation report.",
        content=content,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    # 4. Generate PDF synchronously so pdf_path is immediately ready for download!
    pdf_path = await generate_report_pdf(
        report_id=str(report_id),
        user_name=current_user.full_name,
        content=content,
    )

    return ReportResponse(
        id=str(report.id),
        session_id=report.session_id,
        report_type=report.report_type,
        title=report.title,
        summary=report.summary,
        content=report.content,
        pdf_path=pdf_path or report.pdf_path,
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
        select(Report).where(Report.id == report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # If PDF is not on disk yet, generate it on the fly!
    if not report.pdf_path or not Path(report.pdf_path).exists():
        from services.report_service import generate_report_pdf
        pdf_path = await generate_report_pdf(
            report_id=str(report.id),
            user_name=current_user.full_name,
            content=report.content or {},
        )
        if not pdf_path or not Path(pdf_path).exists():
            raise HTTPException(status_code=500, detail="Could not generate PDF report. Try again.")
        report.pdf_path = pdf_path
        await db.commit()

    return FileResponse(
        path=report.pdf_path,
        media_type="application/pdf",
        filename=f"edupilot_report_{report_id[:8]}.pdf",
    )


@router.post("/email")
@router.post("/email/send")
async def send_report_email_endpoint(
    payload: EmailReportRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send report via Gmail MCP or SMTP to user's email address.
    """
    result = await db.execute(
        select(Report).where(Report.id == payload.report_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    client = GmailMCPClient()
    success = await client.send_report_email(
        report_id=payload.report_id,
        recipient=str(payload.recipient),
        user_name=current_user.full_name,
        subject=payload.subject,
        message=payload.message,
    )

    if success:
        report.email_sent = True
        report.email_sent_at = datetime.now(timezone.utc)
        report.email_recipient = str(payload.recipient)
        await db.commit()
        return {"status": "success", "message": f"Report sent to {payload.recipient}"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Email delivery failed. Please configure SMTP_USERNAME and SMTP_PASSWORD (Gmail App Password) in backend/.env file."
        )
