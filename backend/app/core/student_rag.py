"""
EduPilot AI – Student Data Retrieval-Augmented Generation (RAG) Module.

Retrieves and grounds student profile attributes, academic scores, budget limits,
and uploaded document excerpts (transcripts, SOPs, resumes) to generate 100%
personalized, grounded AI responses tailored to the student's exact data.
"""

import json
from typing import Any, Dict, List, Optional
import structlog

logger = structlog.get_logger(__name__)


def retrieve_student_rag_context(
    profile_data: Dict[str, Any],
    user_query: str,
    document_snippets: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    RAG Context Retriever for Student Data.
    Constructs a grounded RAG context payload containing structured academic profile metrics,
    financial constraints, and document excerpts relevant to the user query.
    """
    cgpa = profile_data.get("cgpa")
    cgpa_scale = profile_data.get("cgpa_scale", 10.0)
    backlogs = profile_data.get("backlogs", 0)
    degree = profile_data.get("degree", "N/A")
    specialization = profile_data.get("specialization", "N/A")
    course_interest = profile_data.get("course_interest", "N/A")
    
    ielts = profile_data.get("ielts_score", "Pending / 0.0")
    toefl = profile_data.get("toefl_score")
    gre = profile_data.get("gre_score")
    
    target_intake = profile_data.get("target_intake", "N/A")
    total_budget_usd = profile_data.get("total_budget_usd")
    preferred_countries = profile_data.get("preferred_countries", [])
    
    # 1. Structured RAG Attributes
    structured_context = {
        "academic_performance": {
            "cgpa": f"{cgpa} / {cgpa_scale}" if cgpa is not None else "Not specified",
            "backlogs_count": backlogs,
            "degree_program": degree,
            "specialization": specialization,
            "field_of_interest": course_interest,
        },
        "test_scores": {
            "ielts_overall": ielts,
            "toefl_score": toefl or "N/A",
            "gre_score": gre or "N/A",
        },
        "financial_constraints": {
            "annual_budget_usd": f"${total_budget_usd:,.0f} USD" if isinstance(total_budget_usd, (int, float)) else "Not specified",
            "full_scholarship_preferred": True if profile_data.get("financial_background") == "scholarship" or "scholarship" in str(user_query).lower() else False,
        },
        "target_preferences": {
            "intake_term": target_intake,
            "preferred_countries": preferred_countries if preferred_countries else ["Not specified"],
        },
    }

    # 2. Filter Relevant Document Snippets (RAG Top-K Retrieval)
    relevant_doc_snippets = []
    if document_snippets:
        q_words = set(str(user_query).lower().split())
        for doc in document_snippets:
            snippet_text = doc.get("content", "")
            doc_type = doc.get("doc_type", "Document")
            # Simple keyword relevance scoring
            overlap = sum(1 for w in q_words if w in snippet_text.lower())
            if overlap > 0 or len(relevant_doc_snippets) < 3:
                relevant_doc_snippets.append({
                    "doc_type": doc_type,
                    "excerpt": snippet_text[:400],
                    "relevance_score": overlap,
                })

    # 3. Formatted Markdown RAG Block for LLM Context Prompt
    formatted_context_str = f"""=== RETRIEVED STUDENT RAG CONTEXT ===
🎓 ACADEMIC PROFILE:
• CGPA: {structured_context['academic_performance']['cgpa']} (Backlogs: {structured_context['academic_performance']['backlogs_count']})
• Degree & Specialization: {structured_context['academic_performance']['degree_program']} in {structured_context['academic_performance']['specialization']}
• Intended Field of Study: {structured_context['academic_performance']['field_of_interest']}

📊 EXAM SCORES & ELIGIBILITY:
• IELTS Band: {structured_context['test_scores']['ielts_overall']}
• GRE Score: {structured_context['test_scores']['gre_score']}

💰 FINANCIAL CONSTRAINTS:
• Annual Budget: {structured_context['financial_constraints']['annual_budget_usd']}
• Full Scholarship Preferred: {structured_context['financial_constraints']['full_scholarship_preferred']}

🎯 TARGET PREFERENCES:
• Target Admission Intake: {structured_context['target_preferences']['intake_term']}
• Preferred Destination Countries: {', '.join(structured_context['target_preferences']['preferred_countries'])}
"""

    if relevant_doc_snippets:
        formatted_context_str += "\n📄 RETRIEVED DOCUMENT EXCERPTS:\n"
        for idx, doc in enumerate(relevant_doc_snippets, 1):
            formatted_context_str += f"[{idx}] {doc['doc_type']}: {doc['excerpt']}\n"

    return {
        "structured_context": structured_context,
        "document_snippets": relevant_doc_snippets,
        "formatted_context": formatted_context_str,
    }
