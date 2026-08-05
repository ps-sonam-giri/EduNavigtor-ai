"""
Report Generation Service
Creates formatted PDF reports using ReportLab.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import structlog

from app.config import settings

logger = structlog.get_logger(__name__)


async def generate_report_pdf(report_id: str, user_name: str, content: Dict[str, Any]) -> str:
    """
    Generate a PDF report from agent output content.
    Returns the file path of the generated PDF.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph, Spacer, Table, TableStyle,
            SimpleDocTemplate, HRFlowable, PageBreak
        )

        reports_dir = Path(settings.reports_dir)
        reports_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = reports_dir / f"report_{report_id}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        brand_color = colors.HexColor("#667eea")
        dark_color = colors.HexColor("#1a1a2e")

        # Custom styles
        title_style = ParagraphStyle(
            "BrandTitle",
            parent=styles["Title"],
            textColor=brand_color,
            fontSize=24,
            spaceAfter=6,
        )
        heading_style = ParagraphStyle(
            "BrandHeading",
            parent=styles["Heading2"],
            textColor=dark_color,
            fontSize=14,
            spaceBefore=16,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BrandBody",
            parent=styles["Normal"],
            fontSize=10,
            leading=16,
        )
        label_style = ParagraphStyle(
            "Label",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#666666"),
        )

        story = []

        # ── Cover ─────────────────────────────────────────────────────────────
        story.append(Spacer(1, 1 * cm))
        story.append(Paragraph("EduPilot AI", title_style))
        story.append(Paragraph("Study Abroad Planning Report", heading_style))
        story.append(Paragraph(f"Prepared for: <b>{user_name}</b>", body_style))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", label_style
        ))
        story.append(HRFlowable(width="100%", thickness=2, color=brand_color, spaceAfter=20))

        # ── Executive Summary ────────────────────────────────────────────────
        if content.get("report_agent", {}).get("executive_summary"):
            story.append(Paragraph("Executive Summary", heading_style))
            story.append(Paragraph(
                content["report_agent"]["executive_summary"].replace("\n", "<br/>"),
                body_style,
            ))
            story.append(Spacer(1, 0.5 * cm))

        # ── Student Profile ───────────────────────────────────────────────────
        profile = content.get("profile_agent", {})
        if profile:
            story.append(Paragraph("Student Profile", heading_style))
            profile_data = profile.get("student_profile", {})
            profile_rows = [
                ["Field", "Value"],
                ["CGPA", f"{profile_data.get('cgpa', 'N/A')} / {profile_data.get('cgpa_scale', 10)}"],
                ["Degree", profile_data.get("degree", "N/A")],
                ["Specialization", profile_data.get("specialization", "N/A")],
                ["IELTS Score", str(profile_data.get("ielts_score", "N/A"))],
                ["GRE Score", str(profile_data.get("gre_score", "N/A"))],
                ["Budget", f"USD {profile_data.get('total_budget_usd', 'N/A'):,}" if isinstance(profile_data.get("total_budget_usd"), (int, float)) else "N/A"],
                ["Course Interest", profile_data.get("course_interest", "N/A")],
                ["Target Intake", profile_data.get("target_intake", "N/A")],
            ]
            t = Table(profile_rows, colWidths=[5 * cm, 12 * cm])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), brand_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5ff")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.5 * cm))

        # ── University Recommendations ────────────────────────────────────────
        uni_data = content.get("university_agent", {})
        universities = uni_data.get("recommended_universities", [])
        if universities:
            story.append(PageBreak())
            story.append(Paragraph("University Recommendations", heading_style))
            for i, uni in enumerate(universities[:5], 1):
                story.append(Paragraph(
                    f"{i}. <b>{uni.get('name', 'N/A')}</b> – {uni.get('country', 'N/A')}",
                    body_style,
                ))
                if uni.get("why_recommended"):
                    story.append(Paragraph(
                        f"<i>{uni['why_recommended']}</i>", label_style
                    ))
                story.append(Paragraph(
                    f"QS Rank: {uni.get('qs_world_rank', 'N/A')} | "
                    f"Tuition: USD {uni.get('avg_tuition_usd_per_year', 'N/A'):,}/yr | "
                    f"Category: {uni.get('category', 'N/A').upper()}",
                    label_style,
                ) if isinstance(uni.get("avg_tuition_usd_per_year"), (int, float)) else
                Paragraph(f"QS Rank: {uni.get('qs_world_rank', 'N/A')}", label_style))
                story.append(Spacer(1, 0.3 * cm))

        # ── Scholarships ──────────────────────────────────────────────────────
        sch_data = content.get("scholarship_agent", {})
        scholarships = sch_data.get("matched_scholarships", [])
        if scholarships:
            story.append(Paragraph("Matched Scholarships", heading_style))
            for s in scholarships[:5]:
                story.append(Paragraph(
                    f"• <b>{s.get('name', 'N/A')}</b> by {s.get('provider', 'N/A')} – "
                    f"{s.get('amount_description', 'N/A')}",
                    body_style,
                ))
                if s.get("why_good_fit"):
                    story.append(Paragraph(f"  {s['why_good_fit']}", label_style))
            story.append(Spacer(1, 0.5 * cm))

        # ── Finance Breakdown ─────────────────────────────────────────────────
        fin_data = content.get("finance_agent", {})
        breakdowns = fin_data.get("finance_breakdown", {}).get("breakdowns", [])
        if breakdowns:
            story.append(PageBreak())
            story.append(Paragraph("Financial Breakdown", heading_style))
            fin_rows = [["University", "Tuition/yr (USD)", "Living/yr (USD)", "Total Year 1 (USD)"]]
            for b in breakdowns[:5]:
                fin_rows.append([
                    b.get("university", "N/A"),
                    f"{b.get('tuition_per_year_usd', 0):,.0f}",
                    f"{b.get('living_cost_per_year_usd', 0):,.0f}",
                    f"{b.get('total_year1_usd', 0):,.0f}",
                ])
            ft = Table(fin_rows, colWidths=[6 * cm, 4 * cm, 4 * cm, 4 * cm])
            ft.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), brand_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0ff")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(ft)

        # ── Timeline ─────────────────────────────────────────────────────────
        tl_data = content.get("timeline_agent", {})
        timeline = tl_data.get("application_timeline", [])
        if timeline:
            story.append(PageBreak())
            story.append(Paragraph("Application Timeline", heading_style))
            for item in timeline:
                story.append(Paragraph(
                    f"<b>{item.get('month_label', f'Month {item.get(\"month_offset\", 0) + 1}')}</b> – "
                    f"{item.get('milestone', 'N/A')} "
                    f"[<font color='#667eea'>{item.get('priority', '').upper()}</font>]",
                    body_style,
                ))
                story.append(Paragraph(item.get("description", ""), label_style))
                story.append(Spacer(1, 0.2 * cm))

        # ── Final Recommendation ──────────────────────────────────────────────
        if content.get("report_agent", {}).get("final_recommendation"):
            story.append(PageBreak())
            story.append(Paragraph("Final Recommendation", heading_style))
            story.append(Paragraph(
                content["report_agent"]["final_recommendation"].replace("\n", "<br/>"),
                body_style,
            ))

        # ── Footer ────────────────────────────────────────────────────────────
        story.append(Spacer(1, 1 * cm))
        story.append(HRFlowable(width="100%", thickness=1, color=brand_color))
        story.append(Paragraph(
            "Generated by EduPilot AI | Powered by Qwen2.5 + LangGraph | "
            "Verify all information with official university sources.",
            label_style,
        ))

        doc.build(story)
        logger.info("PDF report generated", path=str(pdf_path))

        # Update report record with pdf_path
        await _update_report_pdf_path(report_id, str(pdf_path))
        return str(pdf_path)

    except Exception as e:
        logger.error("PDF generation failed", report_id=report_id, error=str(e))
        return ""


async def _update_report_pdf_path(report_id: str, pdf_path: str):
    """Update the report record with the generated PDF path."""
    try:
        import uuid
        from sqlalchemy import update
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.report import Report

        engine = create_async_engine(settings.database_url, echo=False)
        AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

        async with AsyncSession() as session:
            await session.execute(
                update(Report)
                .where(Report.id == uuid.UUID(report_id))
                .values(pdf_path=pdf_path)
            )
            await session.commit()
        await engine.dispose()
    except Exception as e:
        logger.error("Failed to update report pdf_path", error=str(e))
