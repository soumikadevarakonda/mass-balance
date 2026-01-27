import pandas as pd
import numpy as np

# Configuration
SIGMA = 2.0  # analytical variability (%)
INPUT_FILE = "synthetic_forced_degradation_data_500.csv"
OUTPUT_FILE = "synthetic_forced_degradation_data_recomputed.csv"

# Load dataset
df = pd.read_csv(INPUT_FILE)

print("Loaded dataset shape:", df.shape)
print(df.head())

# Recompute total degradants from individual ones
df["Total_degradants_calc"] = df["Degradant_1"] + df["Degradant_2"] + df["Degradant_3"]

# Recompute AMB
df["AMB_calc"] = df["API_remaining"] + df["Total_degradants_calc"]

# Recompute RMB
lost = 100.0 - df["API_remaining"]
df["RMB_calc"] = df["Total_degradants_calc"] / lost

# Recompute Z_MB
df["Z_MB_calc"] = (df["AMB_calc"] - 100.0) / SIGMA

# Show differences vs original (sanity check)
print("\nSanity check (mean absolute differences):")
if "AMB" in df.columns:
    print("AMB diff:", np.mean(np.abs(df["AMB"] - df["AMB_calc"])))
if "RMB" in df.columns:
    print("RMB diff:", np.mean(np.abs(df["RMB"] - df["RMB_calc"])))
if "Z_MB" in df.columns:
    print("Z_MB diff:", np.mean(np.abs(df["Z_MB"] - df["Z_MB_calc"])))

# For the rest of the project, we will use ONLY the recalculated columns.
# Let's rename them to clean names and drop old ones.

df["Total_degradants"] = df["Total_degradants_calc"]
df["AMB"] = df["AMB_calc"]
df["RMB"] = df["RMB_calc"]
df["Z_MB"] = df["Z_MB_calc"]

df = df.drop(columns=[
    "Total_degradants_calc",
    "AMB_calc",
    "RMB_calc",
    "Z_MB_calc"
])

# Save cleaned, recomputed dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nRecomputed dataset saved to:", OUTPUT_FILE)
print(df.head())
