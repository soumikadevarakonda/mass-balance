import pandas as pd
import numpy as np

# =========================
# Configuration
# =========================
INPUT_FILE = "mass_balance_with_diagnostic_zones.csv"
OUTPUT_FILE = "comparative_analysis_summary.csv"

# =========================
# Load data
# =========================
df = pd.read_csv(INPUT_FILE)

print("Loaded dataset:", df.shape)

# =========================
# Classical method decisions
# =========================
df["AMB_Flag"] = np.where(
    (df["AMB"] < 95) | (df["AMB"] > 105),
    "Investigate", "No_Action"
)

df["RMB_Flag"] = np.where(
    (df["RMB"] < 0.8) | (df["RMB"] > 1.2),
    "Investigate", "No_Action"
)

df["AMBD_Flag"] = np.where(
    df["AMBD"].abs() >= 5,
    "Investigate", "No_Action"
)

df["RMBD_Flag"] = np.where(
    df["RMBD"].abs() >= 0.2,
    "Investigate", "No_Action"
)

# =========================
# Proposed framework decision
# =========================
df["ZMB_Flag"] = np.where(
    (df["Z_MB"].abs() >= 1) &
    (df["Diagnostic_Zone"] != "Zone_1_Consistent"),
    "Investigate", "No_Action"
)

# =========================
# Summary counts
# =========================
summary = pd.DataFrame({
    "AMB": df["AMB_Flag"].value_counts(),
    "RMB": df["RMB_Flag"].value_counts(),
    "AMBD": df["AMBD_Flag"].value_counts(),
    "RMBD": df["RMBD_Flag"].value_counts(),
    "Z_MB_Framework": df["ZMB_Flag"].value_counts()
}).fillna(0).astype(int)

print("\nDecision count comparison:")
print(summary)

# =========================
# False-positive proxy
# Classical investigate but Z_MB says no action
# =========================
df["False_Positive_Classical"] = np.where(
    (
        (df["AMB_Flag"] == "Investigate") |
        (df["RMB_Flag"] == "Investigate") |
        (df["AMBD_Flag"] == "Investigate") |
        (df["RMBD_Flag"] == "Investigate")
    ) &
    (df["ZMB_Flag"] == "No_Action"),
    True, False
)

false_positive_rate = df["False_Positive_Classical"].mean() * 100

print(f"\nEstimated false-positive rate avoided by framework: {false_positive_rate:.2f}%")

# =========================
# Save summary
# =========================
summary.to_csv(OUTPUT_FILE)

print("\nComparative analysis saved to:", OUTPUT_FILE)
