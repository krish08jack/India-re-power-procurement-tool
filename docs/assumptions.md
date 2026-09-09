# Model Assumptions

This document describes the major assumptions used in the India Renewable Energy Power Procurement Tool.

Users should review and update these assumptions based on their project, state, regulatory environment and procurement arrangement.

---

# 1. Project Parameters

| Parameter | Description | Unit |
|---|---|---|
| Plant Capacity | Installed renewable energy capacity | MW |
| CUF | Capacity Utilisation Factor | % |
| Project Life | Economic/project operating period | Years |
| CAPEX | Capital expenditure | ₹/MW |
| O&M Cost | Annual operating and maintenance cost | ₹/MW/year |
| Degradation | Annual reduction in renewable generation | % |
| Discount Rate | Rate used for present value calculations | % |

---

# 2. PPA Parameters

| Parameter | Description | Unit |
|---|---|---|
| PPA Tariff | Initial electricity tariff under PPA | ₹/kWh |
| Tariff Escalation | Annual escalation in PPA tariff | % |
| PPA Tenure | Duration of PPA | Years |
| O&M Escalation | Annual increase in O&M costs | % |

---

# 3. Open Access Parameters

Potential Open Access cost components may include:

- Transmission charges
- Wheeling charges
- Cross Subsidy Surcharge
- Additional Surcharges
- Other applicable charges

The applicability and value of these charges should be based on the relevant state regulations and procurement arrangement.

---

# 4. Electricity Demand

The monthly energy matching module uses electricity demand information to assess:

- Direct renewable energy consumption
- Monthly surplus
- Monthly shortfall
- Banking requirement
- Remaining grid requirement

Demand data should ideally represent the electricity consumption profile relevant to the user or project.

---

# 5. Renewable Generation Profile

Renewable generation may vary across months.

The model therefore allows monthly renewable generation to be evaluated rather than relying only on annual generation.

The generation profile should be based on appropriate project or resource assumptions.

---

# 6. Banking Assumptions

Banking calculations depend on:

- Eligible surplus energy
- Banking rules
- Banking period
- Withdrawal rules
- Banking losses, where applicable
- Regulatory restrictions

The applicable state regulatory framework should be checked before using banking results for actual procurement decisions.

---

# 7. Financial Assumptions

Financial calculations use assumptions such as:

- Discount rate
- Project life
- CAPEX
- O&M cost
- PPA tariff
- Tariff escalation
- Generation degradation

Changing these assumptions can materially affect LCOE, NPV, IRR and payback.

---

# 8. Interpretation

Model results should be treated as indicative analytical outputs rather than guaranteed project outcomes.

Actual project economics may differ due to:

- Regulatory changes
- Market conditions
- Financing costs
- Project delays
- Generation variability
- Curtailment
- Grid constraints
- Changes in Open Access charges
- Changes in taxes or other applicable charges
