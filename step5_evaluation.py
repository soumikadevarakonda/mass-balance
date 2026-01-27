import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

INPUT_FILE = "synthetic_forced_degradation_with_decisions.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)

# ==============================
# Part A — Evaluate Zone vs True Case
# ==============================

# Map Predicted_Zone to a simplified predicted class
def zone_to_class(zone):
    if zone == "Zone_1_Good":
        return "consistent"
    elif zone == "Zone_2_Missing_Degradants":
        return "missing"
    elif zone == "Zone_3_Physical_Loss":
        return "physical_loss"
    elif zone == "Zone_4_Overestimation":
        return "overestimation"
    else:
        return "ambiguous"

df["Predicted_Class"] = df["Predicted_Zone"].apply(zone_to_class)

print("\n=== Evaluation of Diagnostic Zones vs Ground Truth ===")
print("\nConfusion Matrix:")
print(confusion_matrix(df["True_case"], df["Predicted_Class"]))

print("\nClassification Report:")
print(classification_report(df["True_case"], df["Predicted_Class"], zero_division=0))

# ==============================
# Part B — Compare with Traditional Rule
# ==============================

# Traditional rule: If AMB < 98 -> Investigate, else Pass
df["Traditional_Flag"] = df["AMB"] < 98

# Our method: Investigate only if decision is not "No Action" or "Borderline"
def our_investigation_flag(decision):
    if decision == "Within_Analytical_Variability_No_Action":
        return False
    if decision == "Borderline_but_Consistent_Monitor":
        return False
    return True

df["Our_Flag"] = df["Final_Decision"].apply(our_investigation_flag)

# Ground truth: which cases really need investigation?
# Consistent cases -> no investigation, others -> investigation
df["True_Investigate"] = df["True_case"] != "consistent"

print("\n=== Comparison: Traditional Rule vs Our Framework ===")

# Confusion matrices
print("\nTraditional Rule Confusion Matrix:")
print(confusion_matrix(df["True_Investigate"], df["Traditional_Flag"]))

print("\nOur Framework Confusion Matrix:")
print(confusion_matrix(df["True_Investigate"], df["Our_Flag"]))

# Simple metrics
def summarize(name, y_true, y_pred):
    tp = ((y_true == True) & (y_pred == True)).sum()
    tn = ((y_true == False) & (y_pred == False)).sum()
    fp = ((y_true == False) & (y_pred == True)).sum()
    fn = ((y_true == True) & (y_pred == False)).sum()
    print(f"\n{name}:")
    print("  TP:", tp, " FP:", fp)
    print("  TN:", tn, " FN:", fn)
    print("  False alarms:", fp)
    print("  Missed problems:", fn)

summarize("Traditional Rule", df["True_Investigate"], df["Traditional_Flag"])
summarize("Our Framework", df["True_Investigate"], df["Our_Flag"])

# ==============================
# Part C — How many unnecessary investigations avoided?
# ==============================

unnecessary_traditional = ((df["True_Investigate"] == False) & (df["Traditional_Flag"] == True)).sum()
unnecessary_ours = ((df["True_Investigate"] == False) & (df["Our_Flag"] == True)).sum()

print("\nUnnecessary investigations:")
print("  Traditional rule:", unnecessary_traditional)
print("  Our framework:", unnecessary_ours)
print("  Reduction:", unnecessary_traditional - unnecessary_ours)
