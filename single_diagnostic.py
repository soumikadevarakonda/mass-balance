def mass_balance_single_case(
    api_assay,
    degradant_a,
    degradant_b,
    degradant_c,
    sigma=5.0
):
    """
    Single-case Mass Balance Diagnostic Engine
    ------------------------------------------
    Inputs:
      api_assay     : API assay (%)
      degradant_a/b/c : individual degradants (%)
      sigma         : analytical variability (%), default = 5%

    Returns:
      dict with full metrics, zone classification, and recommendation
    """

    # ---- Core calculations ----
    total_degradants = degradant_a + degradant_b + degradant_c
    api_loss = 100.0 - api_assay

    SMB = api_assay + total_degradants
    AMB = SMB
    AMBD = abs(AMB - 100.0)

    if api_loss > 0:
        RMB = total_degradants / api_loss
        RMBD = abs(RMB - 1.0)
    else:
        RMB = None
        RMBD = None

    Z_MB = (AMB - 100.0) / sigma

    # ---- Diagnostic zone logic (FROZEN) ----
    if 98 <= AMB <= 102 and RMB is not None and 0.8 <= RMB <= 1.2:
        zone = "Zone 1 – Consistent"
        interpretation = (
            "API loss is well accounted for by detected degradants. "
            "Observed deviation is within analytical variability."
        )
        recommendation = "No investigation required."

    elif AMB < 98 and RMB is not None and RMB < 0.8:
        zone = "Zone 2 – Missing Degradants"
        interpretation = (
            "Observed API loss exceeds detected degradants, suggesting "
            "incomplete degradant detection or co-elution."
        )
        recommendation = "Investigate undetected or non-chromophoric degradants."

    elif AMB < 98 and RMB is not None and 0.8 <= RMB <= 1.2:
        zone = "Zone 3 – Physical Loss"
        interpretation = (
            "API loss is proportional to degradants, but overall mass balance "
            "is low, indicating possible physical loss."
        )
        recommendation = "Investigate volatility, adsorption, or sample handling losses."

    elif AMB > 102 and RMB is not None and RMB > 1.2:
        zone = "Zone 4 – Overestimation"
        interpretation = (
            "Detected degradants exceed API loss, indicating possible "
            "analytical overestimation."
        )
        recommendation = "Review response factors, peak purity, and integration parameters."

    else:
        zone = "Zone 5 – Ambiguous"
        interpretation = (
            "Mass balance metrics show borderline or conflicting behavior."
        )
        recommendation = "Review analytical variability or repeat experiment."

    # ---- Recommendation matrix row (logical summary) ----
    matrix_row = {
        "AMB_status": "High" if AMB > 102 else "Low" if AMB < 98 else "Acceptable",
        "RMB_status": (
            "High" if RMB and RMB > 1.2 else
            "Low" if RMB and RMB < 0.8 else
            "Acceptable"
        ),
        "Action": recommendation
    }

    # ---- Structured output ----
    result = {
        "Input Summary": {
            "API Assay (%)": round(api_assay, 2),
            "API Loss (%)": round(api_loss, 2),
            "Degradant A (%)": round(degradant_a, 2),
            "Degradant B (%)": round(degradant_b, 2),
            "Degradant C (%)": round(degradant_c, 2),
            "Total Degradants (%)": round(total_degradants, 2),
        },
        "Mass Balance Metrics": {
            "SMB / AMB (%)": round(AMB, 2),
            "AMBD (%)": round(AMBD, 2),
            "RMB": round(RMB, 2) if RMB is not None else None,
            "RMBD": round(RMBD, 2) if RMBD is not None else None,
            "Z_MB": round(Z_MB, 2),
        },
        "Diagnostic Interpretation": {
            "Zone": zone,
            "Explanation": interpretation,
            "Final Recommendation": recommendation,
        },
        "Recommendation Matrix Entry": matrix_row
    }

    return result

case = mass_balance_single_case(
    api_assay=82.0,
    degradant_a=3.8,
    degradant_b=2.4,
    degradant_c=1.2,
    sigma=5.0
)

from pprint import pprint
pprint(case)
