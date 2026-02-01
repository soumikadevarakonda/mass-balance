# 📊 Mass Balance Diagnostic Framework for Forced Degradation Studies

**Team BitByBoth**

🔗 **Live Dashboard (Deployed):**  
https://mass-balance-diagnostic-dashboard.streamlit.app/

🔗 **Dashboard Source Repository:**  
https://github.com/ThanushaGali/mass_balance_calculation

🔗 **Core Analysis & Framework Repository (this repo):**  
https://github.com/soumikadevarakonda/mass-balance

---

## 🔍 Problem Statement

In forced degradation studies, **mass balance (MB)** is routinely used to assess whether loss of active pharmaceutical ingredient (API) is adequately explained by detected degradation products.

Despite its importance, mass balance interpretation in practice suffers from:

- Multiple coexisting calculation methods (SMB, AMB, RMB, AMBD, RMBD)
- Fixed acceptance thresholds applied without analytical context
- No explicit treatment of analytical variability
- Subjective and inconsistent investigation triggers

As a result, analysts frequently face **false-positive investigations**, unclear root-cause identification, and inefficient analytical workflows.

The core challenge is **not to invent a new mass balance formula**, but to **interpret existing metrics in a scientifically and regulatorily meaningful way**.

---

## 🎯 Core Insight

> **There is no single “best” mass balance formula.**  
> Reliable interpretation emerges through **joint, uncertainty-aware evaluation** of existing metrics.

---

## 🧠 Proposed Solution: Mass Balance Diagnostic Framework

We propose a **diagnostic and decision-support framework** that optimizes interpretation of *existing* mass balance metrics while remaining fully aligned with regulatory intent.

The framework integrates three complementary layers:

---

### 1️⃣ Uncertainty-Adjusted Mass Balance Index (Z<sub>MB</sub>)

Mass balance deviation is normalized using analytical variability:

\[
Z_{\text{MB}} = \frac{\text{AMB} - 100}{\sigma}
\]

Where:
- **σ (analytical variability)** is derived from *intermediate precision data* during method validation (ICH Q2(R1))
- |Z<sub>MB</sub>| > 2 → ~95% confidence  
- |Z<sub>MB</sub>| > 3 → ~99% confidence  

This converts mass balance from a raw percentage into a **statistically interpretable signal**, separating analytically explainable variability from genuine imbalance.

---

### 2️⃣ AMB–RMB Diagnostic Map (Core Intellectual Contribution)

Absolute Mass Balance (AMB) and Relative Mass Balance (RMB) are jointly interpreted using a **two-dimensional diagnostic map**, enabling mechanistic classification:

| Diagnostic Zone | Interpretation |
|-----------------|----------------|
| High AMB – Normal RMB | Consistent recovery |
| Low AMB – Low RMB | Missing / non-chromophoric degradants |
| Low AMB – Normal RMB | Physical loss (adsorption, volatility) |
| High AMB – High RMB | Analytical overestimation (RRF / integration) |

This joint interpretation explains **why** mass balance fails, not just *that* it fails.

---

### 3️⃣ Recommendation Matrix (Actionable Output)

Each diagnostic zone maps to **specific analytical actions**, such as:

- Orthogonal testing (LC–MS, CAD/ELSD, alternate columns)
- Physical loss assessment (adsorption, headspace analysis)
- Relative response factor (RRF) verification and integration review

This transforms mass balance from a passive metric into an **active decision-support tool**.

---

## 📈 Tracks Addressed

### ✅ Track 1 – Optimization of Mass Balance Interpretation
- Review of existing mass balance formulas
- Identification of their individual limitations
- Proposal of a **joint, uncertainty-aware interpretive strategy**

### ✅ Track 2 – Data-Driven Diagnostic & Recommendation Framework
- Diagnostic zone classification
- Statistical interpretation using Z-index
- Structured, action-oriented recommendations
- Individual case-level analysis capability

---

## 🧪 Data & Validation Strategy

The framework was evaluated using forced degradation datasets designed to reflect realistic analytical practice:

- Multiple APIs with differing intrinsic stability
- Stress conditions: thermal, acidic, basic, oxidative, photolytic
- Multiple time points (forced degradation & stability-like progression)
- Controlled inclusion of:
  - Missing degradant scenarios
  - Physical loss mechanisms
  - Response factor mismatches

This ensures full population of diagnostic zones rather than idealized cases.

---

## 🖥️ Interactive Dashboard

To demonstrate **real-world usability**, an interactive dashboard was developed and deployed.

Users can:
- Input API assay and degradant values
- Automatically compute all mass balance metrics
- Visualize AMB–RMB diagnostic positioning
- Receive clear, structured analytical recommendations

🔗 **Live App:**  
https://mass-balance-diagnostic-dashboard.streamlit.app/

🔗 **Dashboard Code:**  
https://github.com/ThanushaGali/mass_balance_calculation

---


## 📓 Notebook Purpose

`Overview.ipynb` serves as a **technical appendix**, not exploratory analysis.  
It demonstrates:

- Metric computation
- Diagnostic classification
- Recommendation generation for individual cases

All theoretical justification is provided in the report.

---

## 📜 Regulatory Alignment

- **ICH Q1A(R2):** Stability Testing of New Drug Substances and Products  
- **ICH Q2(R1):** Validation of Analytical Procedures  
- **FDA:** Analytical Procedures and Methods Validation Guidance  

The framework **does not alter regulatory expectations**, but strengthens interpretability and consistency.

---

## 🏁 Key Impact

- Reduces false-positive investigations  
- Improves root-cause clarity  
- Saves analytical time and resources  
- Preserves scientific and regulatory transparency  

---

## 👥 Team

**Team BitByBoth**

