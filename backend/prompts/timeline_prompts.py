"""Timeline generation prompts – structured bullet-point output."""

TIMELINE_GENERATION_PROMPT = """You are a study abroad application strategist for Indian students.

Current Date: {current_date}
Target Intake: {target_intake}
Has IELTS: {has_ielts}
Has GRE: {has_gre}

Student Profile:
{profile}

Target Universities (intake months):
{universities}

Scholarships with Deadlines:
{scholarships}

Generate a personalised month-by-month timeline. Respond ONLY with JSON:
{{
  "timeline": [
    {{
      "month_offset": 0,
      "month_label": "Month 1 (August 2024)",
      "phase": "Test Preparation",
      "milestone": "IELTS Enrollment",
      "description": "Enroll in IELTS coaching. Target band 7.0+.",
      "tasks": [
        "Research IELTS coaching centres – British Council or IDP",
        "Book IELTS exam date (3 months from now)",
        "Start daily vocabulary practice (30 mins/day)",
        "Download IELTS preparation materials"
      ],
      "duration_weeks": 2,
      "priority": "critical",
      "category": "test_prep",
      "depends_on": null
    }}
  ],
  "critical_path_summary": "• Month 1-3: Complete IELTS and GRE\\n• Month 4-5: Prepare SOP, LOR, Resume\\n• Month 6-8: Submit university applications\\n• Month 9: Apply for scholarships\\n• Month 11: Receive offers, make decision\\n• Month 12-14: Visa application and pre-departure",
  "target_intake": "{target_intake}",
  "total_duration_months": 10
}}
"""
