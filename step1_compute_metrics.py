import pandas as pd
import numpy as np

# =========================
# Configuration (LOCKED)
# =========================
SIGMA = 5.0  # analytical variability (%)
API_CONTROL = 100.0
DEGRADANT_CONTROL = 0.0

INPUT_FILE = "multi_drug_forced_degradation_dataset.csv"
OUTPUT_FILE = "mass_balance_all_methods_computed.csv"

# =========================
# Load dataset
# =========================
df = pd.read_csv(INPUT_FILE)

print("Loaded dataset shape:", df.shape)


# =========================
# Total Degradants
# =========================
df["Total_Degradants"] = (
    df["Degradant_A"] +
    df["Degradant_B"] +
    df["Degradant_C"]
)

# =========================
# SMB & AMB
# =========================
df["SMB"] = df["API_Assay_Percent"] + df["Total_Degradants"]
df["AMB"] = df["SMB"]

# =========================
# AMBD
# =========================
df["AMBD"] = df["AMB"] - 100.0

# =========================
# RMB (control-normalized)
# =========================
api_loss = API_CONTROL - df["API_Assay_Percent"]

df["RMB"] = np.where(
    api_loss > 0,
    (df["Total_Degradants"] - DEGRADANT_CONTROL) / api_loss,
    np.nan
)

# =========================
# RMBD
# =========================
df["RMBD"] = df["RMB"] - 1.0

# =========================
# Z_MB (proposed)
# =========================
df["Z_MB"] = df["AMBD"] / SIGMA

# =========================
# Basic sanity checks
# =========================
print("\nSanity check ranges:")
print("AMB:", df["AMB"].min(), "to", df["AMB"].max())
print("RMB:", df["RMB"].min(), "to", df["RMB"].max())
print("Z_MB:", df["Z_MB"].min(), "to", df["Z_MB"].max())

# =========================
# Save output
# =========================
df.to_csv(OUTPUT_FILE, index=False)

print("\nAll MB methods computed and saved to:", OUTPUT_FILE)
print(df.head())
