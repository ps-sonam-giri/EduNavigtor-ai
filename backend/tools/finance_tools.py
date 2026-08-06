"""
Financial Breakdown, Currency Conversion & ROI Calculator Tool.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FinancialBreakdownInput(BaseModel):
    university_name: Optional[str] = Field(None, description="Target university name, e.g., 'Technical University of Munich'")
    location: Optional[str] = Field(None, description="City/Location of university, e.g., 'Munich, Germany'")
    course_name: Optional[str] = Field(None, description="Degree course/program name, e.g., 'MSc Computer Science'")
    tuition_usd_per_year: float = Field(..., description="Annual tuition cost in USD")
    living_cost_usd_per_month: float = Field(1000.0, description="Monthly living cost in USD")
    scholarship_deduction_usd: float = Field(0.0, description="Scholarship deduction per year in USD")
    duration_years: float = Field(2.0, description="Duration of degree program in years")
    target_currency: str = Field("INR", description="Currency conversion code (e.g. 'INR')")


async def calculate_financial_breakdown_tool(
    tuition_usd_per_year: float,
    university_name: Optional[str] = None,
    location: Optional[str] = None,
    course_name: Optional[str] = None,
    living_cost_usd_per_month: float = 1000.0,
    scholarship_deduction_usd: float = 0.0,
    duration_years: float = 2.0,
    target_currency: str = "INR",
) -> Dict[str, Any]:
    """
    Calculate full study abroad financial breakdown, scholarship deductions,
    currency conversions (USD to INR @ 87.0), and loan EMI / break-even ROI analysis.
    """
    usd_to_inr = 87.0
    living_usd_per_year = living_cost_usd_per_month * 12.0
    total_year1_usd = tuition_usd_per_year + living_usd_per_year
    net_year1_usd = max(total_year1_usd - scholarship_deduction_usd, 0.0)
    total_degree_usd = net_year1_usd * duration_years

    net_year1_inr = net_year1_usd * usd_to_inr
    total_degree_inr = total_degree_usd * usd_to_inr

    # Estimated Loan EMI (10.5% interest rate for 7 year tenure on 80% loan amount)
    loan_amount_inr = total_degree_inr * 0.80
    annual_rate = 0.105
    monthly_rate = annual_rate / 12.0
    tenure_months = 84

    if loan_amount_inr > 0:
        emi_inr = (loan_amount_inr * monthly_rate * ((1 + monthly_rate) ** tenure_months)) / (
            ((1 + monthly_rate) ** tenure_months) - 1
        )
    else:
        emi_inr = 0.0

    # Estimated post-grad starting salary & break-even payback period
    est_annual_salary_inr = 3500000.0  # Approx ₹35 LPA average entry level abroad
    monthly_savings_inr = (est_annual_salary_inr * 0.40) / 12.0  # 40% savings rate
    break_even_months = (total_degree_inr / monthly_savings_inr) if monthly_savings_inr > 0 else 0

    return {
        "university_name": university_name or "N/A",
        "location": location or "N/A",
        "course_name": course_name or "N/A",
        "tuition_per_year_usd": tuition_usd_per_year,
        "living_cost_per_year_usd": living_usd_per_year,
        "scholarship_deduction_usd": scholarship_deduction_usd,
        "net_cost_year1_usd": net_year1_usd,
        "net_cost_year1_inr": round(net_year1_inr, 2),
        "total_degree_cost_usd": total_degree_usd,
        "total_degree_cost_inr": round(total_degree_inr, 2),
        "exchange_rate_used": f"1 USD = ₹{usd_to_inr} INR",
        "loan_roi_analysis": {
            "estimated_loan_inr": round(loan_amount_inr, 2),
            "estimated_monthly_emi_inr": round(emi_inr, 2),
            "loan_tenure_years": 7,
            "interest_rate_annual": "10.5%",
            "estimated_break_even_years": round(break_even_months / 12.0, 1),
        },
    }
