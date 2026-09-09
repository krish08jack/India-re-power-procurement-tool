# Calculation Formulas

This document describes the key formulas used in the India Renewable Energy Power Procurement Tool.

The tool is designed as a decision-support model for evaluating renewable energy procurement options, project economics and energy matching.

---

# 1. Version 0.1 — Renewable Energy Cost and LCOE

## 1.1 Annual Renewable Energy Generation

Annual electricity generation is calculated using installed capacity, capacity utilisation factor and the number of hours in a year.

### Formula

Annual Generation (MWh/year)

= Installed Capacity (MW) × CUF × 8,760

Where:

- Installed Capacity = renewable energy plant capacity in MW
- CUF = Capacity Utilisation Factor
- 8,760 = hours in a non-leap year

---

## 1.2 Annual Generation in kWh

Annual Generation (kWh/year)

= Annual Generation (MWh/year) × 1,000

---

## 1.3 Capital Recovery Factor

The Capital Recovery Factor (CRF) is used to convert the initial capital investment into an equivalent annualised cost.

### Formula

CRF = [r × (1+r)^n] / [(1+r)^n - 1]

Where:

- r = discount rate
- n = project life in years

---

## 1.4 Annualised Capital Cost

Annualised CAPEX

= CAPEX × CRF

Where:

- CAPEX = initial project capital expenditure
- CRF = Capital Recovery Factor

---

## 1.5 Annual Operating and Maintenance Cost

Annual O&M Cost

= Installed Capacity × O&M Cost per MW per year

---

## 1.6 Levelised Cost of Electricity

The LCOE represents the average cost of generating one unit of electricity over the project lifetime.

### Simplified Formula

LCOE

= (Annualised CAPEX + Annual O&M Cost)
  / Annual Electricity Generation

The result can be converted from ₹/MWh to ₹/kWh by dividing by 1,000.

---

# 2. Open Access Delivered Cost

The delivered renewable electricity cost can include the renewable energy tariff together with applicable network and regulatory charges.

### Conceptual Formula

Delivered RE Cost

= Energy / PPA Cost
+ Transmission Charges
+ Wheeling Charges
+ Cross Subsidy Surcharge
+ Additional Surcharges
+ Other Applicable Charges

The actual components depend on the applicable state regulatory framework and procurement arrangement.

---

# 3. Grid Electricity Cost

Grid electricity cost is represented using the applicable electricity tariff and other relevant charges.

### Formula

Annual Grid Cost

= Grid Energy Consumption × Grid Electricity Cost

Where:

- Grid Energy Consumption = electricity supplied from the grid
- Grid Electricity Cost = applicable cost per unit

---

# 4. Renewable Energy Savings

Savings from renewable procurement can be estimated by comparing renewable electricity procurement cost with the corresponding grid electricity cost.

### Formula

Annual Savings

= Avoided Grid Cost - Renewable Procurement Cost

---

# 5. Version 0.2 — PPA and 25-Year Project Economics

Version 0.2 extends the model to evaluate the financial performance of a renewable energy project over its project life.

---

## 5.1 Annual Generation with Degradation

Renewable energy generation may decline over time due to module degradation.

### Formula

Generation_t

= Generation_1 × (1 - Degradation)^(t-1)

Where:

- Generation_1 = generation in Year 1
- Degradation = annual degradation rate
- t = project year

---

## 5.2 PPA Tariff Escalation

If the PPA tariff increases annually:

Tariff_t

= Tariff_1 × (1 + Escalation Rate)^(t-1)

Where:

- Tariff_1 = initial PPA tariff
- Escalation Rate = annual tariff escalation
- t = project year

---

## 5.3 Annual PPA Revenue

Annual Revenue

= Renewable Energy Sold × PPA Tariff

---

## 5.4 O&M Escalation

If O&M costs increase annually:

O&M_t

= O&M_1 × (1 + O&M Escalation)^(t-1)

---

## 5.5 Annual Project Cash Flow

Simplified project cash flow:

Cash Flow_t

= Revenue_t - O&M_t - Other Project Costs_t

---

## 5.6 Net Present Value

NPV measures the present value of future project cash flows after accounting for the discount rate.

### Formula

NPV

= Σ [Cash Flow_t / (1+r)^t]

Where:

- Cash Flow_t = project cash flow in year t
- r = discount rate
- t = project year

The initial investment is treated separately as the initial project cash outflow.

---

## 5.7 Internal Rate of Return

IRR is the discount rate at which the net present value of the project cash flows equals zero.

### Formula

0

= Σ [Cash Flow_t / (1+IRR)^t]

IRR is calculated using the project's initial investment and subsequent annual cash flows.

---

## 5.8 Simple Payback Period

Simple payback represents the approximate time required for cumulative project cash flow to recover the initial investment.

Payback Period

= Time required for cumulative cash flow to become positive

---

# 6. Version 0.3 — Monthly Energy Matching

Version 0.3 introduces monthly matching between renewable energy generation and electricity demand.

This provides a more detailed assessment than comparing only annual generation and annual consumption.

---

## 6.1 Monthly Electricity Demand

The model uses monthly electricity demand as the electricity requirement to be served.

Demand_m

= Electricity demand during month m

---

## 6.2 Monthly Renewable Generation

Monthly renewable generation depends on installed capacity and the generation profile.

Conceptually:

Monthly Generation_m

= Installed Capacity × Monthly Generation Factor_m

Where the monthly generation factor represents the expected renewable generation during that month.

---

## 6.3 Direct Renewable Energy Use

Renewable generation is first used to meet electricity demand in the same month.

Direct RE Use_m

= MIN(Monthly Generation_m, Demand_m)

---

## 6.4 Monthly Surplus

When renewable generation exceeds demand:

Surplus_m

= MAX(Monthly Generation_m - Demand_m, 0)

---

## 6.5 Monthly Shortfall

When electricity demand exceeds renewable generation:

Shortfall_m

= MAX(Demand_m - Monthly Generation_m, 0)

---

# 7. Energy Banking

Surplus renewable electricity may be carried forward subject to the applicable banking assumptions.

### Conceptual Formula

Closing Bank Balance_m

= Opening Bank Balance_m
+ Eligible Surplus_m
- Bank Withdrawal_m

The actual banking treatment depends on the assumptions and applicable regulatory framework used in the model.

---

## 7.1 Bank Withdrawal

Banked energy can be used to reduce electricity shortfalls in subsequent periods, subject to the modelled banking rules.

Bank Withdrawal_m

= MIN(Available Bank Balance_m, Monthly Shortfall_m)

---

## 7.2 Remaining Grid Requirement

After direct renewable energy and eligible banked energy are considered:

Remaining Grid Requirement_m

= Demand_m
- Direct RE Use_m
- Bank Withdrawal_m

---

# 8. Renewable Energy Share

The renewable energy share represents the proportion of electricity demand served through renewable energy.

### Formula

RE Share (%)

= Renewable Energy Used / Total Electricity Demand × 100

---

# 9. Renewable Energy Utilisation

Renewable energy utilisation measures how much of the generated renewable electricity is actually used.

### Formula

RE Utilisation (%)

= Renewable Energy Used
  / Renewable Energy Generated × 100

---

# 10. Monthly Energy Balance

The overall monthly balance can be represented as:

Energy Balance_m

= Renewable Generation_m
- Electricity Demand_m

A positive value represents a surplus.

A negative value represents a shortfall.

---

# 11. Interpretation of Results

The tool should not be interpreted using a single indicator alone.

Key indicators include:

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

Together, these indicators provide a broader view of renewable energy procurement economics and energy matching.

---

## Important Note

The formulas documented here describe the analytical framework of the tool. Specific calculations may depend on user-defined assumptions, regulatory charges, project configuration and procurement structure.

Users should validate all assumptions and outputs against applicable regulations, tariffs, contracts and project-specific data before using the results for investment or procurement decisions.
