import pandas as pd
import numpy as np

INPUT_FILE = "synthetic_forced_degradation_with_zones.csv"
OUTPUT_FILE = "synthetic_forced_degradation_with_decisions.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)
print(df.head())

# Final decision function (FROZEN RULES)
def final_decision(AMB, RMB, Z_MB, zone):
    # Step 1: Check significance
    if abs(Z_MB) < 1.0:
        return "Within_Analytical_Variability_No_Action"

    # Step 2: Use zone
    if zone == "Zone_1_Good":
        return "Borderline_but_Consistent_Monitor"
    elif zone == "Zone_2_Missing_Degradants":
        return "Missing_Degradants_Improve_Detection"
    elif zone == "Zone_3_Physical_Loss":
        return "Physical_Loss_Investigate_Process"
    elif zone == "Zone_4_Overestimation":
        return "Overestimation_Check_Method"
    else:
        return "Ambiguous_Manual_Review"

# Apply decision logic
df["Final_Decision"] = df.apply(
    lambda row: final_decision(row["AMB"], row["RMB"], row["Z_MB"], row["Predicted_Zone"]),
    axis=1
)

# Show decision counts
print("\nFinal Decision counts:")
print(df["Final_Decision"].value_counts())

# Save result
df.to_csv(OUTPUT_FILE, index=False)

print("\nSaved file:", OUTPUT_FILE)
