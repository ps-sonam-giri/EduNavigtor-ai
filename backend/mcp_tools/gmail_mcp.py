"""
Gmail MCP Client
Sends study abroad reports, recommendations, and reminders via Gmail.
Uses Google Gmail API via OAuth2 credentials.
"""

import base64
import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

import structlog

from app.config import settings

logger = structlog.get_logger(__name__)


class GmailMCPClient:
    """
    Gmail MCP integration for sending reports and notifications.
    Connects to the Gmail MCP server or uses direct Google API as fallback.
    """

    def __init__(self):
        self.mcp_server_url = f"http://localhost:{settings.mcp_gmail_server_port}"

    async def send_report_email(
        self,
        report_id: str,
        recipient: str,
        user_name: str,
        subject: Optional[str] = None,
        message: Optional[str] = None,
    ) -> bool:
        """Send a study abroad report via Gmail."""
        email_subject = subject or f"Your EduPilot AI Study Abroad Report – {user_name}"
        email_body = message or self._build_report_email_body(user_name, report_id)

        try:
            # Try MCP server first
            return await self._send_via_mcp(recipient, email_subject, email_body, report_id)
        except Exception as e:
            logger.warning("Gmail MCP unavailable, trying direct Google API / SMTP", error=str(e))
            sent = await self._send_via_google_api(recipient, email_subject, email_body, report_id)
            if sent:
                return True
            return await self._send_via_smtp(recipient, email_subject, email_body, report_id)

    async def send_university_recommendation(
        self,
        recipient: str,
        user_name: str,
        universities: list,
    ) -> bool:
        """Send university recommendations summary email."""
        subject = f"Your University Recommendations – EduPilot AI"
        body = self._build_university_email_body(user_name, universities)
        return await self._send_via_mcp(recipient, subject, body)

    async def send_reminder(
        self,
        recipient: str,
        user_name: str,
        reminder_type: str,
        deadline: str,
        university_name: str = "",
    ) -> bool:
        """Send application deadline reminder."""
        subject = f"Reminder: {reminder_type} Deadline – {university_name}"
        body = self._build_reminder_body(user_name, reminder_type, deadline, university_name)
        return await self._send_via_mcp(recipient, subject, body)

    async def _send_via_mcp(
        self,
        recipient: str,
        subject: str,
        body: str,
        report_id: Optional[str] = None,
    ) -> bool:
        """Send email through the Gmail MCP server."""
        try:
            import httpx

            payload = {
                "tool": "send_email",
                "arguments": {
                    "to": recipient,
                    "subject": subject,
                    "body": body,
                    "html": True,
                },
            }

            # Attach PDF if available
            if report_id:
                pdf_path = Path(settings.reports_dir) / f"report_{report_id}.pdf"
                if pdf_path.exists():
                    payload["arguments"]["attachments"] = [str(pdf_path)]

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/call",
                    json=payload,
                )
                response.raise_for_status()
                logger.info("Email sent via MCP", recipient=recipient, subject=subject)
                return True
        except Exception as e:
            logger.error("MCP email send failed", error=str(e))
            raise

    async def _send_via_google_api(
        self,
        recipient: str,
        subject: str,
        body: str,
        report_id: Optional[str] = None,
    ) -> bool:
        """Direct Google Gmail API fallback."""
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build

            # Load stored credentials
            creds_file = Path("./gmail_credentials.json")
            if not creds_file.exists():
                logger.error("Gmail credentials not found. Please set up OAuth2.")
                return False

            with open(creds_file) as f:
                creds_data = json.load(f)

            creds = Credentials.from_authorized_user_info(creds_data)
            service = build("gmail", "v1", credentials=creds)

            # Build message
            msg = MIMEMultipart("alternative")
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            # Attach PDF
            if report_id:
                pdf_path = Path(settings.reports_dir) / f"report_{report_id}.pdf"
                if pdf_path.exists():
                    with open(pdf_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=pdf_path.name)
                        part["Content-Disposition"] = f'attachment; filename="{pdf_path.name}"'
                        msg.attach(part)

            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            service.users().messages().send(userId="me", body={"raw": raw}).execute()
            logger.info("Email sent via Google API", recipient=recipient)
            return True
        except Exception as e:
            logger.error("Google API email send failed", error=str(e))
            return False

    async def _send_via_smtp(
        self,
        recipient: str,
        subject: str,
        body: str,
        report_id: Optional[str] = None,
    ) -> bool:
        """Send email directly using SMTP server (e.g. Gmail SMTP)."""
        import os
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication

        smtp_server = settings.smtp_server or os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(settings.smtp_port or os.environ.get("SMTP_PORT", 587))
        smtp_user = settings.smtp_username or os.environ.get("SMTP_USERNAME", "").strip()
        smtp_pass = settings.smtp_password or os.environ.get("SMTP_PASSWORD", "").strip()
        sender = settings.smtp_sender or smtp_user or "noreply@edupilot.ai"

        if not smtp_user or not smtp_pass:
            logger.warning(
                "SMTP credentials not configured in backend/.env. "
                "Please set SMTP_USERNAME and SMTP_PASSWORD to send emails directly."
            )
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"EduPilot AI <{sender}>"
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            if report_id:
                pdf_path = Path(settings.reports_dir) / f"report_{report_id}.pdf"
                if pdf_path.exists():
                    with open(pdf_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=pdf_path.name)
                        part["Content-Disposition"] = f'attachment; filename="{pdf_path.name}"'
                        msg.attach(part)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            logger.info("Email sent successfully via SMTP", recipient=recipient)
            return True
        except Exception as e:
            logger.error("SMTP email send failed", error=str(e))
            return False

    def _build_report_email_body(self, user_name: str, report_id: str) -> str:
        return f"""
        <html><body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">EduPilot AI</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Your Study Abroad Report is Ready</p>
          </div>
          <div style="padding: 30px; background: #f9f9f9; border-radius: 0 0 10px 10px;">
            <p>Dear <strong>{user_name}</strong>,</p>
            <p>Your personalised study abroad planning report has been generated by EduPilot AI.</p>
            <p>The report includes:</p>
            <ul>
              <li>🎓 University Recommendations with detailed reasoning</li>
              <li>💰 Scholarship Opportunities matched to your profile</li>
              <li>📊 Budget & Finance Breakdown</li>
              <li>📅 Personalised Application Timeline</li>
              <li>✅ Final Recommendation and Action Plan</li>
            </ul>
            <p>Please find your full PDF report attached to this email.</p>
            <div style="background: #667eea; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0;">
              <a href="http://localhost:3000/reports/{report_id}" 
                 style="color: white; text-decoration: none; font-weight: bold; font-size: 16px;">
                View Report Online →
              </a>
            </div>
            <p style="color: #666; font-size: 12px;">
              This report was generated by EduPilot AI. The recommendations are based on your profile 
              and our database. Please verify all information with official university sources.
            </p>
          </div>
        </body></html>
        """

    def _build_university_email_body(self, user_name: str, universities: list) -> str:
        uni_list = "".join(
            f"<li><strong>{u.get('name', '')}</strong> – {u.get('country', '')} "
            f"(QS Rank: {u.get('qs_world_rank', 'N/A')})</li>"
            for u in universities[:5]
        )
        return f"""
        <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2>Your University Recommendations – EduPilot AI</h2>
          <p>Dear <strong>{user_name}</strong>,</p>
          <p>Based on your profile, here are your top university recommendations:</p>
          <ul>{uni_list}</ul>
          <p>Log in to EduPilot AI for detailed analysis, comparison, and your full report.</p>
        </body></html>
        """

    def _build_reminder_body(
        self, user_name: str, reminder_type: str, deadline: str, university_name: str
    ) -> str:
        return f"""
        <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2>⏰ Deadline Reminder – EduPilot AI</h2>
          <p>Dear <strong>{user_name}</strong>,</p>
          <p>This is a reminder that your <strong>{reminder_type}</strong> deadline is approaching:</p>
          <div style="background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 8px;">
            <strong>University:</strong> {university_name}<br>
            <strong>Deadline Type:</strong> {reminder_type}<br>
            <strong>Deadline:</strong> {deadline}
          </div>
          <p>Log in to EduPilot AI to track your progress.</p>
        </body></html>
        """
