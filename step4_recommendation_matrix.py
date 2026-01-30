import pandas as pd
import numpy as np

# =========================
# Configuration
# =========================
INPUT_FILE = "mass_balance_with_diagnostic_zones.csv"
OUTPUT_FILE = "mass_balance_with_recommendations.csv"

# =========================
# Load data
# =========================
df = pd.read_csv(INPUT_FILE)

print("Loaded dataset:", df.shape)

# =========================
# Recommendation logic
# =========================
def recommend_action(z_mb, zone):
    if abs(z_mb) < 1:
        return "No_Action_Within_Variability"

    if zone == "Zone_1_Consistent":
        return "Monitor_Borderline_Consistent"

    if zone == "Zone_2_Missing_Degradants":
        return "Investigate_Missing_Degradants"

    if zone == "Zone_3_Physical_Loss":
        return "Investigate_Physical_Loss"

    if zone == "Zone_4_Overestimation":
        return "Investigate_Analytical_Overestimation"

    return "Manual_Review_Ambiguous"

# =========================
# Apply recommendations
# =========================
df["Final_Recommendation"] = df.apply(
    lambda row: recommend_action(row["Z_MB"], row["Diagnostic_Zone"]),
    axis=1
)

# =========================
# Recommendation distribution
# =========================
print("\nRecommendation distribution:")
print(df["Final_Recommendation"].value_counts())

# =========================
# Save output
# =========================
df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset with recommendations saved to:", OUTPUT_FILE)
print(df.head())
