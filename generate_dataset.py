import numpy as np
import pandas as pd

np.random.seed(42)

SIGMA = 2.0  # analytical variability (%)

def split_into_degradants(total, n=3):
    parts = np.random.dirichlet(np.ones(n)) * total
    return parts

rows = []

def generate_case(case_type, n_samples):
    for _ in range(n_samples):
        if case_type == "consistent":
            A = np.random.uniform(88, 98)
            lost = 100 - A
            D = lost + np.random.uniform(-1.0, 1.0)

        elif case_type == "missing":
            A = np.random.uniform(65, 90)
            lost = 100 - A
            D = lost * np.random.uniform(0.3, 0.7)

        elif case_type == "physical_loss":
            A = np.random.uniform(60, 85)
            lost = 100 - A
            D = lost + np.random.uniform(-1.0, 1.0)
            D = D * np.random.uniform(0.7, 0.9)

        elif case_type == "overestimation":
            A = np.random.uniform(85, 95)
            lost = 100 - A
            D = lost * np.random.uniform(1.2, 1.6)

        D = max(D, 0)

        d1, d2, d3 = split_into_degradants(D, 3)

        AMB = A + D
        RMB = D / lost if lost > 0 else np.nan
        Z_MB = (AMB - 100) / SIGMA

        rows.append({
            "API_remaining": round(A, 3),
            "Degradant_1": round(d1, 3),
            "Degradant_2": round(d2, 3),
            "Degradant_3": round(d3, 3),
            "Total_degradants": round(D, 3),
            "AMB": round(AMB, 3),
            "RMB": round(RMB, 3),
            "Z_MB": round(Z_MB, 3),
            "True_case": case_type
        })

# Generate 500 rows total (125 each)
generate_case("consistent", 125)
generate_case("missing", 125)
generate_case("physical_loss", 125)
generate_case("overestimation", 125)

df = pd.DataFrame(rows)

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save CSV
output_file = "synthetic_forced_degradation_data_500.csv"
df.to_csv(output_file, index=False)

print("Dataset generated:", output_file)
print("Shape:", df.shape)
print(df.head())
