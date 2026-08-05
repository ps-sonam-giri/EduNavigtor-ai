"""Scholarship matching prompts – structured bullet-point output."""

SCHOLARSHIP_MATCH_PROMPT = """You are a scholarship advisor for Indian students going abroad.

Student Profile:
{profile}

Target Universities:
{universities}

Available Scholarships:
{scholarships}

Match the student to scholarships and respond ONLY with JSON:
{{
  "matched_scholarships": [
    {{
      "id": "scholarship_id",
      "name": "Scholarship Name",
      "provider": "Provider",
      "amount_usd": 50000,
      "amount_description": "Full tuition + living allowance",
      "scholarship_basis": "Merit-based | Need-based | Country-specific | Research | Athletic | University-specific",
      "eligibility_criteria": "• Minimum CGPA 7.5\\n• Indian nationals only\\n• Must be applying for postgraduate program",
      "eligibility_match": "High|Medium|Low",
      "why_good_fit": "• Your CGPA 8.5 exceeds the 7.5 minimum\\n• Indian nationals specifically eligible\\n• Your target program (CS) is covered",
      "gap_to_address": "• Need 2 years work experience (you have 0)\\n• Requires leadership essay",
      "action_steps": ["Step 1: Prepare leadership essay", "Step 2: Get 3 recommendation letters", "Step 3: Apply by December deadline"],
      "deadline": "December 2024",
      "application_url": "https://...",
      "priority_rank": 1
    }}
  ],
  "total_potential_savings_usd": 75000,
  "advice": "• Apply to Chevening first – highest value for Indian students\\n• JN Tata is easiest to qualify for with your CGPA\\n• Start applications 6 months before deadlines"
}}
"""
