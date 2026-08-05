"""Report schemas."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, field_serializer


class ReportGenerateRequest(BaseModel):
    session_id: str
    report_type: str = "full"
    send_email: bool = False
    email_recipient: Optional[EmailStr] = None


class ReportResponse(BaseModel):
    id: Any
    session_id: str
    report_type: str
    title: str
    summary: Optional[str] = None
    content: Dict[str, Any] = {}
    pdf_path: Optional[str] = None
    email_sent: bool = False
    created_at: str

    @field_serializer('id')
    def serialize_uuid(self, v: Any) -> str:
        return str(v)

    model_config = {"from_attributes": True}


class EmailReportRequest(BaseModel):
    report_id: str
    recipient: EmailStr
    subject: Optional[str] = None
    message: Optional[str] = None
