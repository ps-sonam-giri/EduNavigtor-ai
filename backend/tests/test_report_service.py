"""
Unit tests for Report Generation Service.
"""

import os
import pytest
from services.report_service import generate_report_pdf


@pytest.mark.asyncio
async def test_report_pdf_generation(tmp_path):
    report_id = "test_report_123"
    user_name = "Test Student"
    content = {
        "student_profile": {
            "cgpa": 8.5,
            "degree": "B.Tech",
            "course_interest": "Computer Science",
            "total_budget_usd": 30000,
        },
        "recommended_universities": [
            {
                "name": "Technical University of Munich",
                "country": "Germany",
                "qs_world_rank": 49,
                "avg_tuition_usd_per_year": 600,
                "why_recommended": "Excellent CS program within budget.",
            }
        ],
        "matched_scholarships": [
            {
                "name": "DAAD Study Scholarship",
                "provider": "DAAD",
                "amount_description": "€934/month stipend",
                "why_good_fit": "Strong academic record matches criteria.",
            }
        ],
        "finance_breakdown": {
            "breakdowns": [
                {
                    "university": "Technical University of Munich",
                    "tuition_per_year_usd": 600,
                    "living_cost_per_year_usd": 10800,
                    "total_year1_usd": 11400,
                }
            ]
        },
        "application_timeline": [
            {
                "month_offset": 0,
                "month_label": "Month 1",
                "milestone": "Prepare SOP and LORs",
                "priority": "high",
                "description": "Draft personal statement.",
            }
        ],
        "final_recommendation": "Technical University of Munich is your top recommended choice.",
    }

    # Generate PDF
    pdf_path = await generate_report_pdf(report_id, user_name, content)

    assert pdf_path is not None
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 0


@pytest.mark.asyncio
async def test_report_pdf_generation_with_db_update_assertion():
    from unittest.mock import AsyncMock
    import uuid

    report_id = str(uuid.uuid4())
    user_name = "Test Student"
    content = {"student_profile": {"cgpa": 8.5}}

    mock_db = AsyncMock()
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()

    pdf_path = await generate_report_pdf(report_id, user_name, content, db=mock_db)

    assert pdf_path is not None
    assert os.path.exists(pdf_path)
    # Assert DB update contract execution
    assert mock_db.execute.called
    assert mock_db.commit.called

