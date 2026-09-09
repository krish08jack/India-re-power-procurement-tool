
import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf

from pathlib import Path

css_file = Path("assets/style.css")

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="India RE Power Procurement Tool",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# COMMON FUNCTIONS
# ============================================================

def format_crore(value):

    return f"₹{value / 10_000_000:.2f} crore"


def calculate_lcoe(
    capacity_mw,
    cuf,
    capex_cr_per_mw,
    om_lakh_per_mw_year,
    project_life,
    discount_rate,
    degradation
):

    annual_generation_mwh = (
        capacity_mw * 8760 * cuf
    )

    capex = (
        capacity_mw
        * capex_cr_per_mw
        * 10_000_000
    )

    annual_om = (
        capacity_mw
        * om_lakh_per_mw_year
        * 100_000
    )

    discounted_cost = capex

    discounted_generation = 0

    for year in range(1, project_life + 1):

        generation = (
            annual_generation_mwh
            * (1 - degradation) ** (year - 1)
        )

        discount_factor = (
            1 / (1 + discount_rate) ** year
        )

        discounted_cost += (
            annual_om * discount_factor
        )

        discounted_generation += (
            generation
            * 1000
            * discount_factor
        )

    lcoe = (
        discounted_cost
        / discounted_generation
    )

    return {
        "annual_generation_mwh": annual_generation_mwh,
        "capex": capex,
        "annual_om": annual_om,
        "lcoe": lcoe
    }


# ============================================================
# VERSION 0.1
# SOLAR LCOE + OA + GRID
# ============================================================

def version_01():

    st.title(
        "☀️ Version 0.1 — Solar LCOE + Open Access"
    )

    st.markdown(
        """
        Evaluate the indicative cost of renewable electricity
        supplied through Open Access compared with conventional
        grid electricity.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    st.sidebar.header("☀️ Solar Project")

    capacity_mw = st.sidebar.number_input(
        "Solar Capacity (MW)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="v01_capacity"
    )

    cuf = st.sidebar.slider(
        "Solar CUF (%)",
        10.0,
        35.0,
        23.0,
        0.5,
        key="v01_cuf"
    ) / 100

    capex_cr_per_mw = st.sidebar.number_input(
        "CAPEX (₹ crore/MW)",
        min_value=0.1,
        value=3.5,
        step=0.1,
        key="v01_capex"
    )

    om_lakh_per_mw_year = st.sidebar.number_input(
        "O&M (₹ lakh/MW/year)",
        min_value=0.0,
        value=5.0,
        step=0.5,
        key="v01_om"
    )

    project_life = st.sidebar.number_input(
        "Project Life (years)",
        1,
        40,
        25,
        1,
        key="v01_life"
    )

    discount_rate = st.sidebar.slider(
        "Discount Rate (%)",
        1.0,
        20.0,
        10.0,
        0.5,
        key="v01_discount"
    ) / 100

    degradation = st.sidebar.slider(
        "Annual Degradation (%)",
        0.0,
        2.0,
        0.5,
        0.1,
        key="v01_degradation"
    ) / 100

    st.sidebar.header("🔌 Grid")

    grid_tariff = st.sidebar.number_input(
        "Grid Tariff (₹/kWh)",
        min_value=0.0,
        value=8.20,
        step=0.10,
        key="v01_grid"
    )

    st.sidebar.header("🔗 Open Access Charges")

    transmission_charge = st.sidebar.number_input(
        "Transmission (₹/kWh)",
        min_value=0.0,
        value=0.30,
        step=0.05,
        key="v01_transmission"
    )

    wheeling_charge = st.sidebar.number_input(
        "Wheeling (₹/kWh)",
        min_value=0.0,
        value=0.50,
        step=0.05,
        key="v01_wheeling"
    )

    css = st.sidebar.number_input(
        "CSS (₹/kWh)",
        min_value=0.0,
        value=0.90,
        step=0.05,
        key="v01_css"
    )

    additional_surcharge = st.sidebar.number_input(
        "Additional Surcharge (₹/kWh)",
        min_value=0.0,
        value=0.20,
        step=0.05,
        key="v01_as"
    )

    banking_charge = st.sidebar.number_input(
        "Banking (₹/kWh)",
        min_value=0.0,
        value=0.20,
        step=0.05,
        key="v01_banking"
    )

    other_charges = st.sidebar.number_input(
        "Other Charges (₹/kWh)",
        min_value=0.0,
        value=0.10,
        step=0.05,
        key="v01_other"
    )

    st.sidebar.header("🏭 Consumer")

    annual_consumption_mwh = st.sidebar.number_input(
        "Annual Consumption (MWh)",
        min_value=100.0,
        value=10_000.0,
        step=500.0,
        key="v01_consumption"
    )

    # --------------------------------------------------------
    # LCOE
    # --------------------------------------------------------

    results = calculate_lcoe(
        capacity_mw,
        cuf,
        capex_cr_per_mw,
        om_lakh_per_mw_year,
        int(project_life),
        discount_rate,
        degradation
    )

    annual_generation_mwh = results[
        "annual_generation_mwh"
    ]

    capex = results["capex"]

    annual_om = results["annual_om"]

    lcoe = results["lcoe"]

    total_oa_charges = (
        transmission_charge
        + wheeling_charge
        + css
        + additional_surcharge
        + banking_charge
        + other_charges
    )

    oa_delivered_cost = (
        lcoe
        + total_oa_charges
    )

    renewable_energy_used = min(
        annual_generation_mwh,
        annual_consumption_mwh
    )

    remaining_grid_energy = max(
        annual_consumption_mwh
        - renewable_energy_used,
        0
    )

    grid_cost = (
        annual_consumption_mwh
        * 1000
        * grid_tariff
    )

    renewable_cost = (
        renewable_energy_used
        * 1000
        * oa_delivered_cost
    )

    remaining_grid_cost = (
        remaining_grid_energy
        * 1000
        * grid_tariff
    )

    total_oa_cost = (
        renewable_cost
        + remaining_grid_cost
    )

    annual_savings = (
        grid_cost
        - total_oa_cost
    )

    savings_percent = (
        annual_savings
        / grid_cost
        * 100
        if grid_cost > 0
        else 0
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Solar LCOE",
        f"₹{lcoe:.2f}/kWh"
    )

    col2.metric(
        "OA Delivered Cost",
        f"₹{oa_delivered_cost:.2f}/kWh"
    )

    col3.metric(
        "Annual Savings",
        format_crore(annual_savings)
    )

    col4.metric(
        "Savings",
        f"{savings_percent:.1f}%"
    )

    # --------------------------------------------------------
    # PROJECT SUMMARY
    # --------------------------------------------------------

    st.subheader("Solar Project Summary")

    summary = pd.DataFrame({
        "Parameter": [
            "Solar Capacity",
            "Annual Solar Generation",
            "CAPEX",
            "Annual O&M",
            "Project Life",
            "Discount Rate",
            "Degradation"
        ],
        "Value": [
            f"{capacity_mw:.2f} MW",
            f"{annual_generation_mwh:,.0f} MWh",
            format_crore(capex),
            f"₹{annual_om / 100_000:.2f} lakh/year",
            f"{int(project_life)} years",
            f"{discount_rate * 100:.1f}%",
            f"{degradation * 100:.1f}%"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # OA BREAKDOWN
    # --------------------------------------------------------

    st.subheader("Open Access Cost Breakdown")

    oa_summary = pd.DataFrame({
        "Component": [
            "Solar LCOE",
            "Transmission",
            "Wheeling",
            "CSS",
            "Additional Surcharge",
            "Banking",
            "Other Charges",
            "Total OA Delivered Cost"
        ],
        "₹/kWh": [
            lcoe,
            transmission_charge,
            wheeling_charge,
            css,
            additional_surcharge,
            banking_charge,
            other_charges,
            oa_delivered_cost
        ]
    })

    st.dataframe(
        oa_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # COST COMPARISON
    # --------------------------------------------------------

    st.subheader("Grid vs Renewable Open Access")

    comparison = pd.DataFrame({
        "Scenario": [
            "Grid Only",
            "Renewable OA + Remaining Grid"
        ],
        "Annual Cost (₹ crore)": [
            grid_cost / 10_000_000,
            total_oa_cost / 10_000_000
        ]
    })

    st.bar_chart(
        comparison.set_index("Scenario")
    )


# ============================================================
# VERSION 0.2
# PPA + 25 YEAR ECONOMICS
# ============================================================

def version_02():

    st.title(
        "📈 Version 0.2 — PPA + 25-Year Project Economics"
    )

    st.markdown(
        """
        Evaluate long-term renewable project economics under
        a Power Purchase Agreement.
        """
    )

    st.info(
        "Unlevered project-level model. Debt financing, taxes, "
        "depreciation, DSCR and working capital are excluded."
    )

    st.divider()

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    st.sidebar.header("☀️ Project Inputs")

    capacity_mw = st.sidebar.number_input(
        "Solar Capacity (MW)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="v02_capacity"
    )

    project_life = st.sidebar.number_input(
        "Project Life (years)",
        5,
        40,
        25,
        1,
        key="v02_life"
    )

    cuf = st.sidebar.slider(
        "Solar CUF (%)",
        10.0,
        35.0,
        23.0,
        0.5,
        key="v02_cuf"
    ) / 100

    degradation = st.sidebar.slider(
        "Annual Degradation (%)",
        0.0,
        2.0,
        0.5,
        0.1,
        key="v02_degradation"
    ) / 100

    st.sidebar.header("💰 Capital & O&M")

    capex_cr_per_mw = st.sidebar.number_input(
        "CAPEX (₹ crore/MW)",
        0.1,
        10.0,
        3.5,
        0.1,
        key="v02_capex"
    )

    om_lakh_per_mw_year = st.sidebar.number_input(
        "O&M (₹ lakh/MW/year)",
        0.0,
        20.0,
        5.0,
        0.5,
        key="v02_om"
    )

    om_escalation = st.sidebar.slider(
        "Annual O&M Escalation (%)",
        0.0,
        8.0,
        3.0,
        0.5,
        key="v02_om_escalation"
    ) / 100

    st.sidebar.header("📄 PPA")

    ppa_tariff = st.sidebar.number_input(
        "Starting PPA Tariff (₹/kWh)",
        0.1,
        20.0,
        5.50,
        0.10,
        key="v02_ppa"
    )

    ppa_escalation = st.sidebar.slider(
        "Annual PPA Escalation (%)",
        0.0,
        8.0,
        2.0,
        0.5,
        key="v02_ppa_escalation"
    ) / 100

    discount_rate = st.sidebar.slider(
        "Discount Rate (%)",
        1.0,
        20.0,
        10.0,
        0.5,
        key="v02_discount"
    ) / 100

    # --------------------------------------------------------
    # INITIAL VALUES
    # --------------------------------------------------------

    annual_generation = (
        capacity_mw
        * 8760
        * cuf
    )

    initial_capex = (
        capacity_mw
        * capex_cr_per_mw
        * 10_000_000
    )

    initial_om = (
        capacity_mw
        * om_lakh_per_mw_year
        * 100_000
    )

    # --------------------------------------------------------
    # CASH FLOW MODEL
    # --------------------------------------------------------

    rows = []

    rows.append({
        "Year": 0,
        "Generation (MWh)": 0,
        "PPA Tariff (₹/kWh)": 0,
        "Revenue (₹ crore)": 0,
        "O&M (₹ crore)": 0,
        "Cash Flow (₹ crore)": (
            -initial_capex / 10_000_000
        ),
        "Discount Factor": 1,
        "Discounted Cash Flow (₹ crore)": (
            -initial_capex / 10_000_000
        )
    })

    for year in range(
        1,
        int(project_life) + 1
    ):

        generation = (
            annual_generation
            * (1 - degradation)
            ** (year - 1)
        )

        tariff = (
            ppa_tariff
            * (1 + ppa_escalation)
            ** (year - 1)
        )

        revenue = (
            generation
            * 1000
            * tariff
        )

        om = (
            initial_om
            * (1 + om_escalation)
            ** (year - 1)
        )

        cash_flow = (
            revenue
            - om
        )

        discount_factor = (
            1 / (1 + discount_rate)
            ** year
        )

        discounted_cash_flow = (
            cash_flow
            * discount_factor
        )

        rows.append({
            "Year": year,
            "Generation (MWh)": generation,
            "PPA Tariff (₹/kWh)": tariff,
            "Revenue (₹ crore)": (
                revenue / 10_000_000
            ),
            "O&M (₹ crore)": (
                om / 10_000_000
            ),
            "Cash Flow (₹ crore)": (
                cash_flow / 10_000_000
            ),
            "Discount Factor": discount_factor,
            "Discounted Cash Flow (₹ crore)": (
                discounted_cash_flow
                / 10_000_000
            )
        })

    df = pd.DataFrame(rows)

    # --------------------------------------------------------
    # CUMULATIVE VALUES
    # --------------------------------------------------------

    df[
        "Cumulative Cash Flow (₹ crore)"
    ] = (
        df["Cash Flow (₹ crore)"].cumsum()
    )

    df[
        "Cumulative Discounted Cash Flow (₹ crore)"
    ] = (
        df[
            "Discounted Cash Flow (₹ crore)"
        ].cumsum()
    )

    # --------------------------------------------------------
    # NPV
    # --------------------------------------------------------

    npv = df[
        "Discounted Cash Flow (₹ crore)"
    ].sum()

    # --------------------------------------------------------
    # IRR
    # --------------------------------------------------------

    try:

        irr = npf.irr(
            df[
                "Cash Flow (₹ crore)"
            ].values
        )

    except:

        irr = np.nan

    # --------------------------------------------------------
    # PAYBACK
    # --------------------------------------------------------

    positive = df[
        df[
            "Cumulative Cash Flow (₹ crore)"
        ] >= 0
    ]

    if len(positive) > 0:

        simple_payback = (
            positive.iloc[0]["Year"]
        )

    else:

        simple_payback = np.nan

    discounted_positive = df[
        df[
            "Cumulative Discounted Cash Flow (₹ crore)"
        ] >= 0
    ]

    if len(discounted_positive) > 0:

        discounted_payback = (
            discounted_positive.iloc[0]["Year"]
        )

    else:

        discounted_payback = np.nan

    # --------------------------------------------------------
    # TOTALS
    # --------------------------------------------------------

    total_generation = df[
        "Generation (MWh)"
    ].sum()

    total_revenue = df[
        "Revenue (₹ crore)"
    ].sum()

    total_om = df[
        "O&M (₹ crore)"
    ].sum()

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Initial CAPEX",
        f"₹{initial_capex / 10_000_000:.2f} crore"
    )

    col2.metric(
        "NPV",
        f"₹{npv:.2f} crore"
    )

    col3.metric(
        "IRR",
        f"{irr * 100:.2f}%"
        if not np.isnan(irr)
        else "N/A"
    )

    col4.metric(
        "Simple Payback",
        f"{simple_payback:.0f} years"
        if not np.isnan(simple_payback)
        else "Not achieved"
    )

    # --------------------------------------------------------
    # SECOND KPI
    # --------------------------------------------------------

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Total Generation",
        f"{total_generation:,.0f} MWh"
    )

    col6.metric(
        "Total Revenue",
        f"₹{total_revenue:.2f} crore"
    )

    col7.metric(
        "Total O&M",
        f"₹{total_om:.2f} crore"
    )

    col8.metric(
        "Discounted Payback",
        f"{discounted_payback:.0f} years"
        if not np.isnan(discounted_payback)
        else "Not achieved"
    )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    st.subheader("25-Year Project Cash Flow")

    st.dataframe(
        df.round(3),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    st.subheader("Annual Solar Generation")

    st.line_chart(
        df[
            df["Year"] > 0
        ][
            [
                "Year",
                "Generation (MWh)"
            ]
        ].set_index("Year")
    )

    st.subheader("PPA Tariff Escalation")

    st.line_chart(
        df[
            df["Year"] > 0
        ][
            [
                "Year",
                "PPA Tariff (₹/kWh)"
            ]
        ].set_index("Year")
    )

    st.subheader("Revenue vs O&M")

    st.line_chart(
        df[
            df["Year"] > 0
        ][
            [
                "Year",
                "Revenue (₹ crore)",
                "O&M (₹ crore)"
            ]
        ].set_index("Year")
    )

    st.subheader("Cumulative Cash Flow")

    st.line_chart(
        df[
            [
                "Year",
                "Cumulative Cash Flow (₹ crore)"
            ]
        ].set_index("Year")
    )

    st.subheader(
        "Cumulative Discounted Cash Flow"
    )

    st.line_chart(
        df[
            [
                "Year",
                "Cumulative Discounted Cash Flow (₹ crore)"
            ]
        ].set_index("Year")
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.download_button(
        "⬇️ Download 25-Year Cash Flow",
        df.to_csv(index=False),
        "version_02_25_year_project_economics.csv",
        "text/csv"
    )


# ============================================================
# VERSION 0.3
# MONTHLY LOAD + SOLAR + BANKING
# ============================================================

def version_03():

    st.title(
        "🔋 Version 0.3 — Monthly Load + Solar + Banking"
    )

    st.markdown(
        """
        Model monthly consumer electricity demand, solar generation,
        direct renewable consumption, surplus generation, banking,
        grid shortfall and monthly electricity costs.
        """
    )

    st.warning(
        "Version 0.3 uses a simplified illustrative banking model. "
        "State-specific banking rules, banking deductions, limits "
        "and settlement provisions will be introduced in Version 0.4."
    )

    st.divider()

    # --------------------------------------------------------
    # DEFAULT MONTHLY PROFILES
    # --------------------------------------------------------

    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    demand_shares = [
        0.075,
        0.073,
        0.078,
        0.085,
        0.095,
        0.095,
        0.090,
        0.085,
        0.082,
        0.080,
        0.078,
        0.084
    ]

    solar_shares = [
        0.075,
        0.078,
        0.090,
        0.095,
        0.100,
        0.095,
        0.080,
        0.075,
        0.070,
        0.070,
        0.080,
        0.092
    ]

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.header("🏭 Consumer")

    annual_consumption_mwh = st.sidebar.number_input(
        "Annual Consumption (MWh)",
        min_value=100.0,
        value=10_000.0,
        step=500.0,
        key="v03_consumption"
    )

    # --------------------------------------------------------
    # SOLAR
    # --------------------------------------------------------

    st.sidebar.header("☀️ Solar")

    capacity_mw = st.sidebar.number_input(
        "Solar Capacity (MW)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="v03_capacity"
    )

    cuf = st.sidebar.slider(
        "Solar CUF (%)",
        10.0,
        35.0,
        23.0,
        0.5,
        key="v03_cuf"
    ) / 100

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    st.sidebar.header("💰 Electricity Cost")

    solar_cost = st.sidebar.number_input(
        "Renewable Delivered Cost (₹/kWh)",
        min_value=0.0,
        value=4.44,
        step=0.05,
        key="v03_solar_cost"
    )

    grid_tariff = st.sidebar.number_input(
        "Grid Tariff (₹/kWh)",
        min_value=0.0,
        value=8.20,
        step=0.10,
        key="v03_grid"
    )

    banking_charge = st.sidebar.number_input(
        "Banking Charge (₹/kWh)",
        min_value=0.0,
        value=0.20,
        step=0.05,
        key="v03_banking"
    )

    # --------------------------------------------------------
    # ANNUAL SOLAR GENERATION
    # --------------------------------------------------------

    annual_solar_generation = (
        capacity_mw
        * 8760
        * cuf
    )

    # --------------------------------------------------------
    # MONTHLY DATA
    # --------------------------------------------------------

    df = pd.DataFrame({
        "Month": months,
        "Demand Share": demand_shares,
        "Solar Share": solar_shares
    })

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    df[
        "Consumer Demand (MWh)"
    ] = (
        annual_consumption_mwh
        * df["Demand Share"]
    )

    df[
        "Solar Generation (MWh)"
    ] = (
        annual_solar_generation
        * df["Solar Share"]
    )

    # --------------------------------------------------------
    # DIRECT SOLAR CONSUMPTION
    # --------------------------------------------------------

    df[
        "Direct Solar Consumption (MWh)"
    ] = np.minimum(
        df["Consumer Demand (MWh)"],
        df["Solar Generation (MWh)"]
    )

    # --------------------------------------------------------
    # SOLAR SURPLUS
    # --------------------------------------------------------

    df[
        "Solar Surplus (MWh)"
    ] = np.maximum(
        df["Solar Generation (MWh)"]
        - df["Consumer Demand (MWh)"],
        0
    )

    # --------------------------------------------------------
    # GRID SHORTFALL
    # --------------------------------------------------------

    df[
        "Grid Shortfall Before Banking (MWh)"
    ] = np.maximum(
        df["Consumer Demand (MWh)"]
        - df["Direct Solar Consumption (MWh)"],
        0
    )

    # --------------------------------------------------------
    # BANKING
    # --------------------------------------------------------

    opening_bank = 0

    banking_withdrawals = []

    available_banks = []

    ending_banks = []

    for _, row in df.iterrows():

        available_bank = (
            opening_bank
            + row["Solar Surplus (MWh)"]
        )

        withdrawal = min(
            available_bank,
            row[
                "Grid Shortfall Before Banking (MWh)"
            ]
        )

        ending_bank = (
            available_bank
            - withdrawal
        )

        available_banks.append(
            available_bank
        )

        banking_withdrawals.append(
            withdrawal
        )

        ending_banks.append(
            ending_bank
        )

        opening_bank = ending_bank

    df[
        "Available Banked Energy (MWh)"
    ] = available_banks

    df[
        "Banking Withdrawal (MWh)"
    ] = banking_withdrawals

    # --------------------------------------------------------
    # GRID AFTER BANKING
    # --------------------------------------------------------

    df[
        "Grid Requirement After Banking (MWh)"
    ] = (
        df[
            "Grid Shortfall Before Banking (MWh)"
        ]
        - df[
            "Banking Withdrawal (MWh)"
        ]
    )

    # --------------------------------------------------------
    # ENDING BANK
    # --------------------------------------------------------

    df[
        "Ending Bank Balance (MWh)"
    ] = ending_banks

    # --------------------------------------------------------
    # RENEWABLE ENERGY USED
    # --------------------------------------------------------

    df[
        "Renewable Energy Used (MWh)"
    ] = (
        df[
            "Direct Solar Consumption (MWh)"
        ]
        + df[
            "Banking Withdrawal (MWh)"
        ]
    )

    # --------------------------------------------------------
    # COSTS
    # --------------------------------------------------------

    df[
        "Grid Cost (₹ crore)"
    ] = (
        df[
            "Grid Requirement After Banking (MWh)"
        ]
        * 1000
        * grid_tariff
        / 10_000_000
    )

    df[
        "Renewable Cost (₹ crore)"
    ] = (
        df[
            "Renewable Energy Used (MWh)"
        ]
        * 1000
        * solar_cost
        / 10_000_000
    )

    # Banking charge applied to withdrawals
    df[
        "Banking Cost (₹ crore)"
    ] = (
        df[
            "Banking Withdrawal (MWh)"
        ]
        * 1000
        * banking_charge
        / 10_000_000
    )

    df[
        "Total Cost (₹ crore)"
    ] = (
        df["Grid Cost (₹ crore)"]
        + df["Renewable Cost (₹ crore)"]
        + df["Banking Cost (₹ crore)"]
    )

    # --------------------------------------------------------
    # GRID-ONLY COST
    # --------------------------------------------------------

    df[
        "Grid-Only Cost (₹ crore)"
    ] = (
        df[
            "Consumer Demand (MWh)"
        ]
        * 1000
        * grid_tariff
        / 10_000_000
    )

    # --------------------------------------------------------
    # SAVINGS
    # --------------------------------------------------------

    df[
        "Monthly Savings (₹ crore)"
    ] = (
        df[
            "Grid-Only Cost (₹ crore)"
        ]
        - df[
            "Total Cost (₹ crore)"
        ]
    )

    # --------------------------------------------------------
    # RENEWABLE SHARE
    # --------------------------------------------------------

    df[
        "Renewable Share (%)"
    ] = (
        df[
            "Renewable Energy Used (MWh)"
        ]
        / df[
            "Consumer Demand (MWh)"
        ]
        * 100
    )

    # --------------------------------------------------------
    # ANNUAL TOTALS
    # --------------------------------------------------------

    total_demand = df[
        "Consumer Demand (MWh)"
    ].sum()

    total_solar = df[
        "Solar Generation (MWh)"
    ].sum()

    total_renewable_used = df[
        "Renewable Energy Used (MWh)"
    ].sum()

    total_grid = df[
        "Grid Requirement After Banking (MWh)"
    ].sum()

    total_savings = df[
        "Monthly Savings (₹ crore)"
    ].sum()

    total_grid_only = df[
        "Grid-Only Cost (₹ crore)"
    ].sum()

    annual_savings_percent = (
        total_savings
        / total_grid_only
        * 100
        if total_grid_only > 0
        else 0
    )

    renewable_share = (
        total_renewable_used
        / total_demand
        * 100
        if total_demand > 0
        else 0
    )

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    st.header("📊 Annual Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Annual Demand",
        f"{total_demand:,.0f} MWh"
    )

    col2.metric(
        "Solar Generation",
        f"{total_solar:,.0f} MWh"
    )

    col3.metric(
        "Renewable Share",
        f"{renewable_share:.1f}%"
    )

    col4.metric(
        "Annual Savings",
        f"₹{total_savings:.2f} crore"
    )

    # --------------------------------------------------------
    # SECOND KPI
    # --------------------------------------------------------

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Renewable Energy Used",
        f"{total_renewable_used:,.0f} MWh"
    )

    col6.metric(
        "Grid Requirement",
        f"{total_grid:,.0f} MWh"
    )

    col7.metric(
        "Ending Bank Balance",
        f"{df.iloc[-1]['Ending Bank Balance (MWh)']:,.0f} MWh"
    )

    col8.metric(
        "Savings",
        f"{annual_savings_percent:.1f}%"
    )

    # --------------------------------------------------------
    # MONTHLY ENERGY TABLE
    # --------------------------------------------------------

    st.subheader("Monthly Energy Balance")

    energy_columns = [
        "Month",
        "Consumer Demand (MWh)",
        "Solar Generation (MWh)",
        "Direct Solar Consumption (MWh)",
        "Solar Surplus (MWh)",
        "Banking Withdrawal (MWh)",
        "Grid Requirement After Banking (MWh)",
        "Ending Bank Balance (MWh)",
        "Renewable Energy Used (MWh)"
    ]

    st.dataframe(
        df[energy_columns].round(2),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # MONTHLY COST TABLE
    # --------------------------------------------------------

    st.subheader("Monthly Cost & Savings")

    cost_columns = [
        "Month",
        "Grid Cost (₹ crore)",
        "Renewable Cost (₹ crore)",
        "Banking Cost (₹ crore)",
        "Total Cost (₹ crore)",
        "Grid-Only Cost (₹ crore)",
        "Monthly Savings (₹ crore)",
        "Renewable Share (%)"
    ]

    st.dataframe(
        df[cost_columns].round(3),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # CHART 1
    # --------------------------------------------------------

    st.subheader("Monthly Demand vs Solar Generation")

    chart_energy = df[
        [
            "Month",
            "Consumer Demand (MWh)",
            "Solar Generation (MWh)"
        ]
    ].set_index("Month")

    st.line_chart(
        chart_energy
    )

    # --------------------------------------------------------
    # CHART 2
    # --------------------------------------------------------

    st.subheader("Monthly Grid Requirement")

    chart_grid = df[
        [
            "Month",
            "Grid Requirement After Banking (MWh)"
        ]
    ].set_index("Month")

    st.bar_chart(
        chart_grid
    )

    # --------------------------------------------------------
    # CHART 3
    # --------------------------------------------------------

    st.subheader("Banking Balance")

    chart_bank = df[
        [
            "Month",
            "Ending Bank Balance (MWh)"
        ]
    ].set_index("Month")

    st.line_chart(
        chart_bank
    )

    # --------------------------------------------------------
    # CHART 4
    # --------------------------------------------------------

    st.subheader("Monthly Savings")

    chart_savings = df[
        [
            "Month",
            "Monthly Savings (₹ crore)"
        ]
    ].set_index("Month")

    st.bar_chart(
        chart_savings
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    st.subheader("🔍 Model Validation")

    # Consumer-side energy balance
    consumer_balance = (
        df[
            "Consumer Demand (MWh)"
        ]
        - (
            df[
                "Renewable Energy Used (MWh)"
            ]
            + df[
                "Grid Requirement After Banking (MWh)"
            ]
        )
    ).abs().max()

    # Generation-side energy balance
    generation_balance = (
        df[
            "Solar Generation (MWh)"
        ]
        - (
            df[
                "Renewable Energy Used (MWh)"
            ]
            + df[
                "Ending Bank Balance (MWh)"
            ]
        )
    ).abs().max()

    st.write(
        f"Consumer-side energy balance error: "
        f"**{consumer_balance:.6f} MWh**"
    )

    st.write(
        f"Generation-side energy balance error: "
        f"**{generation_balance:.6f} MWh**"
    )

    if (
        consumer_balance < 0.000001
        and generation_balance < 0.000001
    ):

        st.success(
            "✓ Energy balance validation passed."
        )

    else:

        st.error(
            "Energy balance validation failed."
        )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.download_button(
        "⬇️ Download Monthly Analysis",
        df.to_csv(index=False),
        "version_03_monthly_load_solar_banking.csv",
        "text/csv"
    )

    # --------------------------------------------------------
    # NOTE
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "Version 0.3 uses illustrative monthly demand and solar "
        "profiles and a simplified banking mechanism. Regulatory "
        "rules and actual state-specific settlement provisions "
        "will be incorporated in Version 0.4."
    )


# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.title("⚡ Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Version 0.1 — LCOE + OA",
        "Version 0.2 — PPA Economics",
        "Version 0.3 — Monthly Analysis"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "India RE Power Procurement Tool"
)

st.sidebar.caption(
    "Prototype: Versions 0.1–0.3"
)


# ============================================================
# ROUTING
# ============================================================

if page == "Version 0.1 — LCOE + OA":

    version_01()

elif page == "Version 0.2 — PPA Economics":

    version_02()

elif page == "Version 0.3 — Monthly Analysis":

    version_03()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Prototype analytical tool | Versions 0.1, 0.2 and 0.3"
)
