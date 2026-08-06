"""
Academic Transcript Document OCR & Extraction Tool.
"""

import re
from typing import Any, Dict
from pydantic import BaseModel, Field


class TranscriptExtractionInput(BaseModel):
    file_path: str = Field(..., description="File path to the uploaded student transcript or scorecard PDF")


async def extract_transcript_data_tool(file_path: str) -> Dict[str, Any]:
    """
    Extract CGPA, IELTS scores, degree, backlogs, and academic profile from uploaded transcript file.
    """
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        return {"error": f"Failed to parse document PDF: {str(e)}"}

    text_upper = text.upper()

    # Extract CGPA
    cgpa_match = re.search(r'(?:CGPA|GRADE|PERCENTAGE|GPA)[:\s]*([0-9]\.[0-9]{1,2}|[1-9][0-9]\.?[0-9]?)', text_upper)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else None

    # Extract IELTS
    ielts_match = re.search(r'IELTS[:\s]*([4-9]\.?[0-5]?)', text_upper)
    ielts = float(ielts_match.group(1)) if ielts_match else None

    # Extract Backlogs
    backlog_match = re.search(r'(?:BACKLOGS?|FAILURES?|ARREARS?)[:\s]*([0-9]+)', text_upper)
    backlogs = int(backlog_match.group(1)) if backlog_match else 0

    # Extract Degree
    degree = "B.Tech / B.E." if "ENGINEERING" in text_upper or "B.TECH" in text_upper or "BACHELOR" in text_upper else "Bachelor Degree"

    return {
        "cgpa": cgpa,
        "cgpa_scale": 10.0 if (cgpa and cgpa <= 10.0) else 4.0,
        "ielts_score": ielts,
        "backlogs": backlogs,
        "degree": degree,
        "extracted_text_preview": text[:300],
        "source": f"Parsed Document: {file_path}",
    }
