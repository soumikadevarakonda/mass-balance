import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "mass_balance_with_recommendations.csv"
OUTPUT_DIR = "figures/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# ===============================
# FIGURE 1 — AMB–RMB MAP (ALL DATA)
# ===============================
plt.figure(figsize=(12, 9))

zone_colors = {
    "Zone_1_Consistent": "green",
    "Zone_2_Missing_Degradants": "red",
    "Zone_3_Physical_Loss": "orange",
    "Zone_4_Overestimation": "purple",
    "Zone_5_Ambiguous": "gray"
}

for zone, color in zone_colors.items():
    subset = df[df["Diagnostic_Zone"] == zone]
    if not subset.empty:
        plt.scatter(
            subset["RMB"],
            subset["AMB"],
            color=color,
            label=zone,
            s=120,
            alpha=0.8
        )

plt.axhline(95, linestyle="--", color="black")
plt.axhline(105, linestyle="--", color="black")
plt.axvline(0.8, linestyle="--", color="black")
plt.axvline(1.2, linestyle="--", color="black")

plt.xlabel("Relative Mass Balance (RMB)")
plt.ylabel("Absolute Mass Balance (AMB)")
plt.title("AMB–RMB Diagnostic Map Across All APIs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "figure1_amb_rmb_all.png", dpi=300)
plt.show()

# ===============================
# FIGURE 2 — Z_MB DISTRIBUTION BY API
# ===============================
plt.figure(figsize=(10, 7))

apis = df["API_Name"].unique()
zmb_data = [df[df["API_Name"] == api]["Z_MB"] for api in apis]

plt.boxplot(zmb_data, tick_labels=apis, showfliers=True)
plt.axhline(1, linestyle="--", color="red")
plt.axhline(-1, linestyle="--", color="red")

plt.xlabel("API")
plt.ylabel("Z_MB")
plt.title("Z_MB Distribution Across APIs")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "figure2_zmb_by_api.png", dpi=300)
plt.show()

# ===============================
# FIGURE 3 — VISUAL RECOMMENDATION MATRIX
# ===============================
matrix = pd.crosstab(df["Diagnostic_Zone"], df["Final_Recommendation"])

plt.figure(figsize=(12, 6))
plt.imshow(matrix, cmap="Blues")
plt.colorbar(label="Count")

plt.xticks(range(len(matrix.columns)), matrix.columns, rotation=45, ha="right")
plt.yticks(range(len(matrix.index)), matrix.index)

for i in range(len(matrix.index)):
    for j in range(len(matrix.columns)):
        plt.text(j, i, matrix.iloc[i, j], ha="center", va="center")

plt.title("Recommendation Matrix: Zone vs Action")
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "figure3_recommendation_matrix.png", dpi=300)
plt.show()

# ===============================
# FIGURE 4 — COMPARATIVE ANALYSIS (RECOMPUTED)
# ===============================
methods = {
    "AMB": ((df["AMB"] < 95) | (df["AMB"] > 105)),
    "RMB": ((df["RMB"] < 0.8) | (df["RMB"] > 1.2)),
    "AMBD": (df["AMBD"].abs() >= 5),
    "RMBD": (df["RMBD"].abs() >= 0.2),
    "Z_MB_Framework": (df["Z_MB"].abs() >= 1)
}

counts = [cond.sum() for cond in methods.values()]

plt.figure(figsize=(10, 6))
plt.bar(methods.keys(), counts)
plt.ylabel("Number of Investigations")
plt.title("Comparison of Investigation Triggers")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "figure4_comparative_analysis.png", dpi=300)
plt.show()

print("STEP 5 COMPLETED SUCCESSFULLY — ALL FIGURES GENERATED")
