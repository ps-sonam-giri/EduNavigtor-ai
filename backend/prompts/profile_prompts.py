"""Student profile extraction and summary prompts."""

PROFILE_EXTRACTION_PROMPT = """You are a study abroad advisor for Indian students. Extract student profile information from the user query.

Existing Profile:
{existing_profile}

User Query: "{user_query}"

Extract ONLY fields explicitly mentioned. Return JSON:
{{
  "cgpa": null,
  "cgpa_scale": 10,
  "backlogs": 0,
  "degree": null,
  "specialization": null,
  "graduation_year": null,
  "ielts_score": null,
  "toefl_score": null,
  "gre_score": null,
  "gmat_score": null,
  "preferred_countries": [],
  "course_interest": null,
  "career_goal": null,
  "target_intake": null,
  "total_budget_usd": null,
  "financial_background": null,
  "work_experience_years": 0
}}
"""

PROFILE_SUMMARY_PROMPT = """You are an expert study abroad counsellor for Indian students.
Create a concise profile summary using bullet points.

Profile Data:
{profile}

Write a structured summary in this format:

**Academic Background**
• Degree: [degree] in [specialization] from [university]
• CGPA: [cgpa]/[scale] | Backlogs: [backlogs]
• Graduation: [year]

**Test Scores**
• IELTS: [score] | GRE: [score] | TOEFL: [score]

**Study Goals**
• Target: [course_interest] | Intake: [target_intake]
• Preferred countries: [countries]
• Career goal: [career_goal]

**Finance**
• Budget: USD [amount] | Source: [financial_background]

Use bullet points only. Fill N/A if data is missing.
"""
