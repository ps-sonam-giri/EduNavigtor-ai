"""Report generation prompts – structured bullet-point output."""

EXECUTIVE_SUMMARY_PROMPT = """You are a senior study abroad counsellor writing a report for an Indian student.

Profile Summary: {profile_summary}
Top 3 Universities: {top_universities}
Top 3 Scholarships: {top_scholarships}
Finance Summary: {finance_summary}
Timeline Phases: {timeline_phases}

Write a structured executive summary using EXACTLY this format:

**Student Overview**
• [Student's academic background and goals in 1-2 sentences]

**Top University Picks**
• [University 1]: [One sentence why it fits this student]
• [University 2]: [One sentence why it fits this student]
• [University 3]: [One sentence why it fits this student]

**Scholarship Opportunities**
• [Scholarship 1]: [Amount and why eligible]
• [Scholarship 2]: [Amount and why eligible]

**Financial Snapshot**
• Total estimated cost: [amount]
• Scholarship savings potential: [amount]
• Net cost: [amount]

**Next Steps**
• [Action 1]
• [Action 2]
• [Action 3]

Use bullet points throughout. Be specific with numbers. Do NOT use paragraphs.
"""

FINAL_RECOMMENDATION_PROMPT = """You are a senior study abroad counsellor giving a final recommendation to an Indian student.

Student Profile: {profile}
Career Goal: {career_goal}
Top Universities: {universities}
Scholarships: {scholarships}
Finance: {finance}

Give your final recommendation using EXACTLY this format:

**🏆 Top Recommendation**
• University: [Name], [Country]
• Why: [2-3 specific reasons referencing student's CGPA, budget, career goal]
• Program: [Recommended program]
• Total Cost: [USD amount per year]

**⚠️ Why Not the Others**
• [University 2]: [Specific reason it ranks lower for THIS student]
• [University 3]: [Specific reason it ranks lower for THIS student]

**✅ Action This Week**
• [Single most important action the student must take right now]

**🔴 Key Risk to Watch**
• [One specific risk for this student's application]

Use bullet points only. Be direct and specific.
"""
