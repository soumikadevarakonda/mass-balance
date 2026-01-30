import pandas as pd

# =========================
# Configuration
# =========================
INPUT_FILE = "mass_balance_all_methods_computed.csv"
OUTPUT_FILE = "mass_balance_with_diagnostic_zones.csv"

# =========================
# Load data
# =========================
df = pd.read_csv(INPUT_FILE)

print("Loaded dataset:", df.shape)
print(df.head())

# =========================
# Diagnostic Zone Rules
# (AMB–RMB Map)
# =========================
def classify_zone(AMB, RMB):
    # Zone 1: Good mass balance
    if 95 <= AMB <= 105 and 0.8 <= RMB <= 1.2:
        return "Zone_1_Consistent"

    # Zone 2: Missing degradants
    elif AMB < 95 and RMB < 0.8:
        return "Zone_2_Missing_Degradants"

    # Zone 3: Physical loss / volatility
    elif AMB < 95 and 0.8 <= RMB <= 1.2:
        return "Zone_3_Physical_Loss"

    # Zone 4: Overestimation / analytical artifact
    elif AMB > 105 and RMB > 1.2:
        return "Zone_4_Overestimation"

    # Borderline / ambiguous
    else:
        return "Zone_5_Ambiguous"

# =========================
# Apply classification
# =========================
df["Diagnostic_Zone"] = df.apply(
    lambda row: classify_zone(row["AMB"], row["RMB"]),
    axis=1
)

# =========================
# Zone distribution
# =========================
print("\nDiagnostic Zone Counts:")
print(df["Diagnostic_Zone"].value_counts())

# =========================
# Save output
# =========================
df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset with diagnostic zones saved to:", OUTPUT_FILE)
print(df.head())
