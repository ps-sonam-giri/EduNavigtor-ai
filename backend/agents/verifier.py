"""
Reflection & Verification Node.

Audits candidate agent outputs against hard constraints:

1. CGPA eligibility
2. Budget compliance
3. Factual grounding in raw tool observations
4. Target country exclusivity
"""

import re
from typing import Any, Dict, List, Set

from agents.state import AgentState


# ============================================================
# COUNTRY CONFIGURATION
# ============================================================

KNOWN_COUNTRIES = [
    "germany",
    "usa",
    "uk",
    "canada",
    "australia",
    "ireland",
    "japan",
    "singapore",
    "new zealand",
]


# ============================================================
# OBSERVATION EXTRACTION
# ============================================================

def _extract_observed_names_and_urls(
    observations: List[Dict[str, Any]]
) -> tuple[Set[str], Set[str]]:
    """
    Extract university/scholarship names and URLs
    from raw tool observations.
    """

    observed_names: Set[str] = set()
    observed_urls: Set[str] = set()

    for obs in observations:
        data = obs.get("observation", [])

        if isinstance(data, list):

            for item in data:
                if isinstance(item, dict):

                    if "name" in item:
                        observed_names.add(
                            str(item["name"]).lower()
                        )

                    if "title" in item:
                        observed_names.add(
                            str(item["title"]).lower()
                        )

                    if "url" in item:
                        observed_urls.add(
                            str(item["url"]).lower()
                        )

        elif isinstance(data, dict):

            if "results" in data and isinstance(
                data["results"], list
            ):

                for res in data["results"]:

                    if isinstance(res, dict):

                        if "title" in res:
                            observed_names.add(
                                str(res["title"]).lower()
                            )

                        if "url" in res:
                            observed_urls.add(
                                str(res["url"]).lower()
                            )

    return observed_names, observed_urls


# ============================================================
# TARGET COUNTRY DETECTION
# ============================================================

def _get_target_country(
    state: AgentState
) -> str | None:
    """
    Determine the active target country.

    Priority:
    1. Country explicitly mentioned in user query
    2. Student preferred country
    """

    user_q = str(
        state.get("user_query", "")
    ).lower()

    # --------------------------------------------------------
    # 1. Explicit country in user query
    # --------------------------------------------------------

    for country in KNOWN_COUNTRIES:

        if country in user_q:
            return country

    # --------------------------------------------------------
    # 2. Preferred country from student profile
    # --------------------------------------------------------

    profile = state.get(
        "student_profile",
        {}
    )

    preferred_countries = profile.get(
        "preferred_countries",
        []
    )

    if preferred_countries:

        return str(
            preferred_countries[0]
        ).lower()

    return None


# ============================================================
# TARGET COUNTRY EXCLUSIVITY CHECK
# ============================================================

def _check_target_country_exclusivity(
    candidate_message: str,
    target_country: str,
    user_query: str = "",
    profile_country: str = None,
) -> List[str]:
    """
    Ensure that the candidate response answers strictly grounded in student profile target country.
    If query country differs from profile_country and message doesn't guide user to /profile or /compare, flag violation.
    """
    violations: List[str] = []
    text = candidate_message.lower()

    # 1. Profile Country Mismatch Check
    if profile_country and target_country and profile_country.lower() != target_country.lower():
        # If user asked for a different country than their profile target
        has_redirect = any(link in text for link in ["/profile", "my profile", "/compare", "compare"])
        if not has_redirect:
            violations.append(
                f"Profile Target Mismatch: Student profile target country is set to '{profile_country.title()}', "
                f"but user requested '{target_country.title()}'. Inform the user that their active target country is '{profile_country.title()}', "
                f"and direct them to [My Profile](/profile) to update their target country or to [Compare Tab](/compare) for multi-country comparisons."
            )

    # 2. Exclusivity check against unselected countries
    target_country_clean = target_country.lower().strip()
    for country in KNOWN_COUNTRIES:
        if country == target_country_clean:
            continue
        if country in text and country not in user_query.lower() and not any(link in text for link in ["/profile", "/compare"]):
            violations.append(
                f"Unselected Country Mention: Active requested target country is "
                f"'{target_country.title()}', but the response mentions unselected country "
                f"'{country.title()}'. Remove all references to unselected countries."
            )

    return violations


# ============================================================
# VERIFIER NODE
# ============================================================

async def verifier_node(
    state: AgentState
) -> AgentState:
    """
    Audits accumulated agent state and final candidate message.

    Checks:

    1. CGPA eligibility
    2. Budget compliance
    3. Dollar claims
    4. Web-search citation requirement
    5. Target country exclusivity
    6. Factual grounding against observations
    """

    profile = state.get(
        "student_profile",
        {}
    )

    unis = state.get(
        "recommended_universities",
        []
    )

    observations = state.get(
        "observations",
        []
    )

    candidate_message = state.get(
        "message",
        ""
    )

    violations: List[str] = []

    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    student_cgpa = float(
        profile.get("cgpa") or 0.0
    )

    student_budget = float(
        profile.get(
            "total_budget_usd"
        ) or 999999.0
    )

    # ========================================================
    # 1. CGPA VERIFICATION
    # ========================================================

    for university in unis:

        min_cgpa = float(
            university.get(
                "min_cgpa"
            ) or 0.0
        )

        if (
            min_cgpa > 0
            and student_cgpa > 0
            and student_cgpa < min_cgpa
        ):

            violations.append(
                f"CGPA Violation: Recommended university "
                f"'{university.get('name')}' requires minimum "
                f"CGPA {min_cgpa}, but student CGPA is only "
                f"{student_cgpa}."
            )

    # ========================================================
    # 2. BUDGET VERIFICATION
    # ========================================================

    for university in unis:

        tuition = float(
            university.get(
                "avg_tuition_usd_per_year"
            ) or 0.0
        )

        if tuition > student_budget:

            violations.append(
                f"Budget Violation: University "
                f"'{university.get('name')}' tuition "
                f"(${tuition:,.0f}/yr) exceeds student "
                f"budget (${student_budget:,.0f}/yr)."
            )

    # ========================================================
    # 3. MESSAGE CLAIM INSPECTION
    # ========================================================

    if candidate_message:

        # ----------------------------------------------------
        # Dollar amount verification
        # ----------------------------------------------------

        dollar_amounts = re.findall(
            r'\$(\d{1,3}(?:,\d{3})+|\d+)',
            candidate_message
        )

        for amt_str in dollar_amounts:

            val = float(
                amt_str.replace(",", "")
            )

            if (
                val > student_budget
                and val < 200000
                and "budget"
                not in candidate_message.lower()
            ):

                # Ignore known multi-year / ROI references.
                if not any(
                    keyword in candidate_message.lower()
                    for keyword in [
                        "total loan",
                        "roi",
                        "payback",
                        "2-year",
                        "two year",
                    ]
                ):

                    violations.append(
                        f"Message Claim Violation: Text mentions "
                        f"expense of ${val:,.0f} which exceeds "
                        f"student budget of "
                        f"${student_budget:,.0f}."
                    )

        # ----------------------------------------------------
        # Tavily citation verification
        # ----------------------------------------------------

        tavily_ran = any(
            obs.get("tool") == "tavily_search"
            for obs in observations
        )

        if tavily_ran:

            has_citations = any(
                citation in candidate_message
                for citation in [
                    "http://",
                    "https://",
                    "[Source:",
                    "[Apply",
                    "[Website",
                ]
            )

            if (
                not has_citations
                and len(candidate_message) > 50
            ):

                violations.append(
                    "Citation Requirement: Web search facts "
                    "are included in the message, but inline "
                    "claim-level citations "
                    "([Source: Domain](URL)) are missing."
                )

        # ====================================================
        # 4. TARGET COUNTRY EXCLUSIVITY
        # ====================================================

        target_country = _get_target_country(state)

        if target_country:
            pref_countries = profile.get("preferred_countries", [])
            profile_cntry = pref_countries[0] if pref_countries else None

            country_violations = (
                _check_target_country_exclusivity(
                    candidate_message=candidate_message,
                    target_country=target_country,
                    user_query=state.get("user_query", ""),
                    profile_country=profile_cntry,
                )
            )

            violations.extend(
                country_violations
            )

    # ========================================================
    # 5. GROUNDING VERIFICATION
    # ========================================================

    observed_names, observed_urls = (
        _extract_observed_names_and_urls(
            observations
        )
    )

    if unis and observed_names:

        for university in unis:

            university_name = str(
                university.get("name", "")
            ).lower()

            if (
                university_name
                and not any(
                    observed_name in university_name
                    or university_name in observed_name
                    for observed_name in observed_names
                )
            ):

                violations.append(
                    f"Grounding Warning: "
                    f"'{university.get('name')}' was not "
                    f"returned by database or search "
                    f"observations."
                )

    # ========================================================
    # EXECUTION TRACE
    # ========================================================

    executed = list(
        state.get(
            "agents_executed",
            []
        )
    )

    executed.append(
        "verifier"
    )

    # ========================================================
    # VERIFIER FAILED
    # ========================================================

    if violations:

        critique = (
            "Verifier Reflection & Constraint Violations:\n"
            + "\n".join(
                f"• {violation}"
                for violation in violations
            )
        )

        return {
            **state,
            "verifier_passed": False,
            "verifier_critique": critique,
            "agents_executed": executed,
        }

    # ========================================================
    # VERIFIER PASSED
    # ========================================================

    return {
        **state,
        "verifier_passed": True,
        "verifier_critique": (
            "All constraints and textual claims "
            "verified successfully."
        ),
        "agents_executed": executed,
    }