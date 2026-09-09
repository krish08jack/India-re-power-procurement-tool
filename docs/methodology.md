# Methodology

## 1. Overview

The India Renewable Energy Power Procurement Tool is designed as a decision-support tool for evaluating renewable energy procurement options in India.

The analytical framework progressively moves from cost assessment to project economics and finally to monthly energy matching.

The tool currently integrates:

1. Version 0.1 — Renewable energy cost and LCOE analysis
2. Version 0.2 — PPA and 25-year project economics
3. Version 0.3 — Monthly energy matching and banking

---

# 2. Overall Analytical Framework

The tool follows the following analytical sequence:

User Inputs
        ↓
Renewable Energy Generation
        ↓
Cost and LCOE Analysis
        ↓
Open Access / Grid Comparison
        ↓
PPA Economics
        ↓
25-Year Cash Flow
        ↓
Monthly Energy Matching
        ↓
Surplus / Shortfall
        ↓
Banking
        ↓
Procurement Indicators

---

# 3. Version 0.1 Methodology

Version 0.1 establishes the basic economics of renewable electricity procurement.

The analysis starts with the renewable energy plant configuration.

Key inputs include:

- Plant capacity
- CUF
- CAPEX
- O&M cost
- Project life
- Discount rate
- Grid electricity cost
- Open Access charges

The model estimates annual renewable electricity generation and calculates the levelised cost of electricity.

The renewable electricity cost can then be compared with the applicable grid electricity cost and Open Access procurement cost.

### Main outputs

- Annual renewable generation
- LCOE
- Renewable procurement cost
- Grid electricity cost
- Open Access cost
- Estimated savings

---

# 4. Version 0.2 Methodology

Version 0.2 builds on Version 0.1 by introducing long-term project economics.

The project is evaluated over a 25-year period.

For each project year, the model considers:

- Renewable generation
- Generation degradation
- PPA tariff
- PPA tariff escalation
- Revenue
- O&M cost
- O&M escalation
- Project cash flow

The resulting cash flows are used to estimate:

- NPV
- IRR
- Payback period

This allows users to assess both the cost of electricity and the financial performance of the underlying renewable energy project.

---

# 5. Version 0.3 Methodology

Version 0.3 introduces monthly energy matching.

Instead of assuming that annual renewable generation directly offsets annual electricity demand, the model compares generation and demand at a monthly level.

For each month:

1. Renewable generation is calculated.
2. Electricity demand is identified.
3. Renewable generation is first used to meet demand.
4. Surplus renewable energy is identified.
5. Monthly shortfall is identified.
6. Eligible surplus may be added to the energy bank.
7. Banked energy may be used to meet future shortfalls.
8. Remaining electricity demand is supplied through the grid or other procurement arrangements.

This approach provides a more realistic representation of temporal renewable energy utilisation.

---

# 6. Integrated Procurement Analysis

The three versions are designed to work together.

Version 0.1 answers:

"How does renewable electricity compare with grid electricity on cost?"

Version 0.2 answers:

"What are the long-term economics of the renewable energy project?"

Version 0.3 answers:

"How well does renewable generation match electricity demand over time?"

Together, these provide a broader procurement decision-support framework.

---

# 7. Key Decision Indicators

The integrated tool provides indicators including:

- LCOE
- Delivered renewable electricity cost
- Grid electricity cost
- Annual savings
- NPV
- IRR
- Payback period
- Renewable energy share
- Renewable energy utilisation
- Monthly surplus
- Monthly shortfall
- Banking requirement
- Remaining grid requirement

---

# 8. Limitations

The tool is a decision-support prototype.

Results depend on:

- User-defined assumptions
- Renewable generation profile
- Electricity demand profile
- PPA structure
- Applicable Open Access charges
- Banking rules
- Regulatory conditions
- Project-specific costs

The tool does not replace detailed project due diligence, legal review, regulatory assessment or financial modelling.

---

# 9. Future Development

Potential future development areas include:

- Wind power
- Hybrid renewable projects
- Battery energy storage
- More detailed hourly matching
- Demand profiles
- Multiple procurement structures
- State-specific regulatory parameters
- Sensitivity analysis
- Scenario analysis
- Advanced financial modelling
