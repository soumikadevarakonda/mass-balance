import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "synthetic_forced_degradation_with_decisions.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)
print(df.head())

# ==============================
# 1. AMB vs RMB Diagnostic Map
# ==============================

plt.figure(figsize=(8, 6))

zone_colors = {
    "Zone_1_Good": "green",
    "Zone_2_Missing_Degradants": "orange",
    "Zone_3_Physical_Loss": "blue",
    "Zone_4_Overestimation": "red",
    "Ambiguous": "gray"
}

for zone, color in zone_colors.items():
    sub = df[df["Predicted_Zone"] == zone]
    if len(sub) > 0:
        plt.scatter(sub["AMB"], sub["RMB"], label=zone, alpha=0.6, s=25, c=color)

# Draw zone boundaries
plt.axvline(98, color="black", linestyle="--")
plt.axvline(100, color="black", linestyle=":")
plt.axvline(102, color="black", linestyle="--")

plt.axhline(0.8, color="black", linestyle="--")
plt.axhline(1.0, color="black", linestyle=":")
plt.axhline(1.2, color="black", linestyle="--")

plt.xlabel("Absolute Mass Balance (AMB)")
plt.ylabel("Relative Mass Balance (RMB)")
plt.title("AMB–RMB Diagnostic Map")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("plot_amb_rmb_diagnostic_map.png", dpi=150)
plt.show()

# ==============================
# 2. Z_MB Distribution Plot
# ==============================

plt.figure(figsize=(8, 5))

plt.hist(df["Z_MB"], bins=40, alpha=0.7)

# Draw significance lines
plt.axvline(-1, color="red", linestyle="--", label="±1σ")
plt.axvline(1, color="red", linestyle="--")

plt.axvline(-2, color="purple", linestyle=":", label="±2σ")
plt.axvline(2, color="purple", linestyle=":")

plt.xlabel("Z_MB")
plt.ylabel("Count")
plt.title("Distribution of Z_MB (Uncertainty-Normalized MB Deviation)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("plot_zmb_distribution.png", dpi=150)
plt.show()

# ==============================
# 3. Final Decision Distribution
# ==============================

plt.figure(figsize=(10, 5))

df["Final_Decision"].value_counts().plot(kind="bar")

plt.ylabel("Count")
plt.title("Distribution of Final Decisions")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.grid(axis="y")

plt.savefig("plot_final_decision_distribution.png", dpi=150)
plt.show()

print("\nPlots saved:")
print(" - plot_amb_rmb_diagnostic_map.png")
print(" - plot_zmb_distribution.png")
print(" - plot_final_decision_distribution.png")
