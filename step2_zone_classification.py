import pandas as pd

INPUT_FILE = "synthetic_forced_degradation_data_recomputed.csv"
OUTPUT_FILE = "synthetic_forced_degradation_with_zones.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)
print(df.head())

# Zone classification function (FROZEN RULES)
def classify_zone(AMB, RMB):
    if 98 <= AMB <= 102 and 0.8 <= RMB <= 1.2:
        return "Zone_1_Good"
    elif AMB < 98 and RMB < 0.8:
        return "Zone_2_Missing_Degradants"
    elif AMB < 98 and 0.8 <= RMB <= 1.2:
        return "Zone_3_Physical_Loss"
    elif AMB > 102 and RMB > 1.2:
        return "Zone_4_Overestimation"
    else:
        return "Ambiguous"

# Apply classification
df["Predicted_Zone"] = df.apply(lambda row: classify_zone(row["AMB"], row["RMB"]), axis=1)

# Show counts
print("\nZone counts:")
print(df["Predicted_Zone"].value_counts())

# Save result
df.to_csv(OUTPUT_FILE, index=False)

print("\nSaved file:", OUTPUT_FILE)
