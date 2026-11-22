def check_eligibility(scheme, age=None, state="", income=None, occupation="", category=""):
    """Return cautious, rules-aware preliminary guidance, not a decision."""
    scheme_id = scheme.get("id", "")
    reasons = []
    missing = []
    result = "Insufficient information"
    if scheme_id == "pmuy":
        if age is None: missing.append("Age")
        if not occupation: missing.append("Household LPG/occupation context")
        if age is not None and age < 18:
            result = "Likely does not meet the minimum age criterion"
            reasons.append("PMUY guidance states the applicant must be a woman aged 18 or older.")
        elif age is not None and age >= 18:
            reasons.append("Age meets the 18+ threshold, but applicant must be a woman, belong to a qualifying poor household, and have no household LPG connection.")
            result = "Potentially relevant; key criteria need confirmation"
    elif scheme_id == "pm-kisan":
        missing.append("Landholding and exclusion details; current portal verification")
        reasons.append("The scheme covers eligible landholding farmer families, subject to exclusions and official validation.")
        result = "Check official beneficiary status"
    else:
        missing.append("Scheme-specific criteria and beneficiary database check")
        reasons.append("The selected scheme uses criteria that are not fully represented in this quick checker.")
    return {"result": result, "reasons": reasons, "missing": missing, "documents": scheme.get("documents", []), "next_steps": scheme.get("application_steps", []), "official_url": scheme.get("official_url")}
