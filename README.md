# India Renewable Energy Power Procurement Tool

An open-source decision-support tool for analysing renewable energy procurement options in India.
a
The tool brings together renewable energy cost analysis, open-access comparison, long-term PPA economics, and monthly energy matching with banking into a single Streamlit application.

https://india-re-power-procurement-tool-v1.streamlit.app/
---

## About the Tool

The India Renewable Energy Power Procurement Tool is designed to help users evaluate different renewable electricity procurement options from both a cost and project-economics perspective.

The tool currently integrates three analytical modules:

- Version 0.1 – Solar LCOE and Open Access comparison
- Version 0.2 – PPA and 25-year project economics
- Version 0.3 – Monthly energy matching and banking
- Version 0.4 – Regulatory & Open Access Analysis
The objective is to progressively develop the tool into a practical decision-support platform for renewable energy procurement and power planning in India.
India-re-power-procurement-tool/
│
├── app.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
│
├── src/
│   └── regulatory_engine.py
│
├── data/
│   └── processed/
│       └── regulatory/
│           ├── rajasthan_regulatory_parameters.csv
│           └── rajasthan_tariff_parameters.csv
│
├── assets/
└── docs/
  
## How the Tool Works

The three versions are integrated into a single analytical workflow.

```text
                    INDIA RE POWER PROCUREMENT TOOL
                               │
                               ▼
                     Project & User Inputs
                               │
                               ▼
              ┌────────────────────────────────┐
              │                                │
              │       VERSION 0.1              │
              │   Solar LCOE + OA + Grid       │
              │       Comparison               │
              │                                │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │                                │
              │       VERSION 0.2              │
              │   PPA + 25-Year Economics      │
              │                                │
              │ Revenue • Cash Flow • NPV      │
              │ IRR • Payback                  │
              │                                │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │                                │
              │       VERSION 0.3              │
              │ Monthly Energy Matching        │
              │       + Banking                │
              │                                │
              │ Solar Generation               │
              │ Demand Matching               │
              │ Surplus / Shortfall            │
              │ Banking / Withdrawal           │
              │                                │
              └───────────────┬────────────────┘
                              │
                              ▼
                   INTEGRATED RESULTS
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             Cost        Project         Energy
           Comparison    Economics       Matching
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                     Procurement Insights

Version 0.1 – Solar LCOE + Open Access Comparison
Version 0.1 provides a basic comparison of renewable energy procurement costs.
Key Inputs
Solar plant capacity
Capacity Utilisation Factor (CUF)
Capital expenditure (CAPEX)
Operations and maintenance (O&M)
Project life
Discount rate
Solar degradation
Grid tariff
Open Access charges
Key Outputs
Levelised Cost of Electricity (LCOE)
Annual renewable generation
Delivered renewable energy cost
Open Access cost
Grid electricity cost
Estimated savings
Renewable energy share
The purpose of Version 0.1 is to establish the basic cost competitiveness of renewable electricity compared with conventional grid procurement.

## Version 0.2 – PPA + 25-Year Project Economics
Version 0.2 extends the analysis from a simple cost comparison to a long-term project economics model.
The module evaluates the financial performance of a renewable energy project over a 25-year project life.
Key Components
Annual renewable generation
Solar degradation
PPA tariff
Tariff escalation
O&M costs
O&M escalation
Annual revenue
Annual project costs
Cash flow
Net Present Value (NPV)
Internal Rate of Return (IRR)
Simple payback period
Discounted payback period
This allows users to assess both the cost of renewable electricity and the underlying economics of the project.

Version 0.3 – Monthly Energy Matching + Banking
Version 0.3 introduces a more detailed energy-balance approach.
Instead of assuming that annual renewable generation automatically offsets annual electricity consumption, the model evaluates energy generation and demand on a monthly basis.

Analytical Flow
Monthly Electricity Demand
            +
Monthly Solar Generation
            │
            ▼
     Direct Solar Use
            │
      ┌─────┴─────┐
      ▼           ▼
   Surplus     Shortfall
      │           │
      ▼           ▼
   Banking     Grid / OA
      │
      ▼
Bank Withdrawal
      │
      ▼
Renewable Energy Used
      │
      ▼
Remaining Grid Requirement
      │
      ▼
Cost & Savings Analysis
Key Outputs
Monthly electricity demand
Monthly solar generation
Direct renewable energy consumption
Monthly surplus
Monthly shortfall
Energy banked
Energy withdrawn from bank
Renewable energy utilised
Remaining grid requirement
Annual renewable energy share
Energy cost comparison
Estimated savings
Monthly and annual energy balance
Version 0.3 therefore provides a more realistic representation of how renewable electricity interacts with electricity demand over time.

Documentation

Detailed documentation for the tool is available below:

- [Calculation Formulas](docs/formulas.md)
- [Analytical Methodology](docs/methodology.md)
- [Model Assumptions](docs/assumptions.md)
- [User Guide](docs/user_guide.md)


