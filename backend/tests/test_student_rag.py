"""
Unit tests for Student Data RAG Retrieval Module.
"""

import pytest
from app.core.student_rag import retrieve_student_rag_context


def test_retrieve_student_rag_context_formatting():
    profile = {
        "cgpa": 5.6,
        "cgpa_scale": 10.0,
        "backlogs": 2,
        "degree": "BCA",
        "specialization": "Computer Science",
        "ielts_score": 0.0,
        "total_budget_usd": 20000,
        "preferred_countries": ["Australia"],
        "target_intake": "Spring 2027",
    }
    user_query = "suggest me universities for AI"

    rag = retrieve_student_rag_context(profile, user_query)

    assert "structured_context" in rag
    assert "formatted_context" in rag
    
    fmt = rag["formatted_context"]
    assert "RETRIEVED STUDENT RAG CONTEXT" in fmt
    assert "5.6 / 10.0" in fmt
    assert "Backlogs: 2" in fmt
    assert "Australia" in fmt
    assert "$20,000 USD" in fmt
