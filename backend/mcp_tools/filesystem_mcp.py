"""
Filesystem MCP Client
Reads uploaded student documents (PDF, DOCX) and extracts information.
Supports: resume, marksheet, IELTS scorecard, SOP.
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)


class FilesystemMCPClient:
    """
    Reads local files via MCP filesystem server or direct extraction.
    Extracts structured data from student documents.
    """

    async def extract_from_document(
        self, file_path: str, doc_type: str
    ) -> Dict[str, Any]:
        """
        Extract structured information from a document.
        doc_type: resume | marksheet | ielts | sop
        """
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        suffix = path.suffix.lower()

        try:
            if suffix == ".pdf":
                text = await self._extract_pdf_text(file_path)
            elif suffix in {".docx", ".doc"}:
                text = await self._extract_docx_text(file_path)
            elif suffix in {".txt", ".md"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
            else:
                return {"error": f"Unsupported file type: {suffix}"}

            # Use LLM to extract structured data
            return await self._llm_extract(text, doc_type)

        except Exception as e:
            logger.error("Document extraction failed", path=file_path, error=str(e))
            return {"error": str(e)}

    async def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using pypdf."""
        try:
            import pypdf

            reader = pypdf.PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except ImportError:
            # Fallback: try pdfminer
            try:
                from pdfminer.high_level import extract_text as pdfminer_extract
                return pdfminer_extract(file_path)
            except ImportError:
                return f"[PDF extraction unavailable. Install pypdf: pip install pypdf]"

    async def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX."""
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            return "[DOCX extraction unavailable. Install python-docx]"

    async def _llm_extract(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Use LLM to extract structured data from document text."""
        from agents.llm import ainvoke_llm, extract_json_from_response

        # Trim text to avoid token overflow
        trimmed = text[:3000] if len(text) > 3000 else text

        prompts = {
            "resume": f"""Extract the following from this resume text:
- full_name
- email  
- work_experience_years (total years)
- skills (list of key technical skills)
- degree (highest degree)
- university_name
- graduation_year
- cgpa (if mentioned)

Resume text:
{trimmed}

Return JSON only.""",
            "marksheet": f"""Extract the following from this academic transcript/marksheet:
- cgpa (overall CGPA or percentage)
- cgpa_scale (4.0 or 10.0 etc.)
- degree
- specialization
- university_name
- graduation_year
- backlogs (number of backlogs/arrears if mentioned)
- subjects (list of subjects with grades if available)

Marksheet text:
{trimmed}

Return JSON only.""",
            "ielts": f"""Extract the following from this IELTS scorecard:
- ielts_score (overall band score)
- listening (band score)
- reading (band score)  
- writing (band score)
- speaking (band score)
- test_date
- candidate_name

Scorecard text:
{trimmed}

Return JSON only.""",
            "sop": f"""Analyse this Statement of Purpose and extract:
- course_interest (the program/field they're applying for)
- career_goal (stated career objective)
- preferred_countries (countries mentioned as targets)
- key_strengths (list of mentioned strengths/achievements)

SOP text:
{trimmed}

Return JSON only.""",
        }

        prompt = prompts.get(doc_type, f"Extract all relevant information from this document:\n{trimmed}\nReturn JSON only.")
        response_text, _ = await ainvoke_llm(prompt)
        extracted = extract_json_from_response(response_text)

        # Rule-based fallback for CGPA/IELTS if LLM fails
        if not extracted:
            extracted = self._rule_based_extract(text, doc_type)

        return extracted

    def _rule_based_extract(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Simple regex-based extraction as last resort."""
        result: Dict[str, Any] = {}

        if doc_type == "ielts":
            match = re.search(r"overall.*?(\d\.\d)", text, re.IGNORECASE)
            if match:
                result["ielts_score"] = float(match.group(1))

        if doc_type in ("marksheet", "resume"):
            match = re.search(r"cgpa.*?(\d+\.?\d*)", text, re.IGNORECASE)
            if match:
                result["cgpa"] = float(match.group(1))

        return result
