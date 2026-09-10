
import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
from pathlib import Path
from src.regulatory_engine import RegulatoryEngine

# ============================================================
# REGULATORY DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

REGULATORY_DB = (
    BASE_DIR
    / "data"
    / "processed"
    / "regulatory"
    / "rajasthan_regulatory_parameters.csv"
)

TARIFF_DB = (
    BASE_DIR
    / "data"
    / "processed"
    / "regulatory"
    / "rajasthan_tariff_parameters.csv"
)

regulatory_engine = RegulatoryEngine(
    REGULATORY_DB,
    TARIFF_DB
)
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
# VERSION 0.4
# RAJASTHAN REGULATORY + TARIFF ENGINE
# ============================================================

def _regulatory_value(parameter_id, state="Rajasthan", **kwargs):
    """
    Retrieve a regulatory parameter from the regulatory engine.

    The regulatory engine returns a DataFrame, so this helper
    extracts the applicable value for display.
    """
    try:
        result = regulatory_engine.get_parameter(
            state=state,
            parameter_id=parameter_id,
            **{
                k: v for k, v in kwargs.items()
                if v is not None
            }
        )

        if result is None or result.empty:
            return None

        # Return the first applicable value.
        return result.iloc[0]["Value"]

    except Exception as e:
        return None


def _tariff_lookup(
    parameter,
    state="Rajasthan",
    voltage_level=None,
    effective_date="2026-04-01"
):
    """
    Retrieve a tariff value from the tariff engine.

    get_single_tariff_value() returns a dictionary:
    {
        found: bool,
        value: ...,
        unit: ...,
        record: ...,
        message: ...
    }
    """
    try:
        result = regulatory_engine.get_single_tariff_value(
            state=state,
            parameter=parameter,
            voltage_level=voltage_level,
            effective_date=effective_date
        )

        if not isinstance(result, dict):
            return {
                "found": False,
                "value": None,
                "unit": None,
                "record": None,
                "message": "Unexpected tariff engine response."
            }

        return result

    except Exception as e:
        return {
            "found": False,
            "value": None,
            "unit": None,
            "record": None,
            "message": str(e)
        }


def _tariff_value(result):
    """Extract numerical value from tariff lookup result."""
    if isinstance(result, dict) and result.get("found"):
        return result.get("value")
    return None


def _tariff_source_text(result):
    """Create a readable source/traceability string."""
    if not isinstance(result, dict):
        return "Source metadata not available"

    record = result.get("record")

    if not isinstance(record, dict):
        return "Source metadata not available"

    parts = []

    if record.get("Document"):
        parts.append(f"Document: {record['Document']}")

    if record.get("Clause"):
        parts.append(f"Clause: {record['Clause']}")

    if pd.notna(record.get("Page")):
        parts.append(f"Page: {int(record['Page'])}")

    if record.get("Status"):
        parts.append(f"Status: {record['Status']}")

    if record.get("Notes"):
        parts.append(f"Notes: {record['Notes']}")

    return " | ".join(parts) if parts else "Source metadata not available"


def _display_value(value, unit=""):
    """Format a regulatory/tariff value for display."""
    if value is None:
        return "Not available"

    if isinstance(value, float) and np.isnan(value):
        return "Not available"

    if isinstance(value, (int, float, np.integer, np.floating)):
        if unit == "%":
            return f"{float(value):.2f}%"

        if unit:
            return f"{float(value):.2f} {unit}"

        return f"{float(value):.2f}"

    return str(value)


def version_04():

    st.title("📘 Version 0.4 — Rajasthan Regulatory + Tariff Engine")

    st.markdown(
        """
        Evaluate renewable electricity procurement under Rajasthan's
        Green Energy Open Access framework using the project's
        regulatory and tariff databases.
        """
    )

    st.info(
        "Version 0.4 uses the Rajasthan regulatory and tariff databases. "
        "Where a numerical tariff is not available, the model does not assume zero."
    )

    st.divider()

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    st.sidebar.header("📍 Regulatory Context")

    state = st.sidebar.selectbox(
        "State",
        ["Rajasthan"],
        key="v04_state"
    )

    consumer_type = st.sidebar.selectbox(
        "Consumer Type",
        ["Non-Captive", "Captive"],
        key="v04_consumer_type"
    )

    voltage_level = st.sidebar.selectbox(
        "Voltage Level",
        ["11 kV", "33 kV", "132 kV+", "LT"],
        index=0,
        key="v04_voltage"
    )

    st.sidebar.header("☀️ Renewable Project")

    capacity_mw = st.sidebar.number_input(
        "Solar Capacity (MW)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="v04_capacity"
    )

    cuf = st.sidebar.slider(
        "Solar CUF (%)",
        10.0,
        35.0,
        23.0,
        0.5,
        key="v04_cuf"
    ) / 100

    capex_cr_per_mw = st.sidebar.number_input(
        "CAPEX (₹ crore/MW)",
        min_value=0.1,
        value=3.5,
        step=0.1,
        key="v04_capex"
    )

    om_lakh_per_mw_year = st.sidebar.number_input(
        "O&M (₹ lakh/MW/year)",
        min_value=0.0,
        value=5.0,
        step=0.5,
        key="v04_om"
    )

    st.sidebar.header("🏭 Consumer")

    contract_demand_mw = st.sidebar.number_input(
        "Contract Demand (MW)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="v04_contract_demand"
    )

    annual_consumption_mwh = st.sidebar.number_input(
        "Annual Consumption (MWh)",
        min_value=100.0,
        value=10_000.0,
        step=500.0,
        key="v04_consumption"
    )

    st.sidebar.header("💰 Grid Tariff")

    grid_tariff = st.sidebar.number_input(
        "Grid Tariff (₹/kWh)",
        min_value=0.0,
        value=8.20,
        step=0.10,
        key="v04_grid"
    )

    # --------------------------------------------------------
    # BASIC PROJECT ECONOMICS
    # --------------------------------------------------------

    results = calculate_lcoe(
        capacity_mw,
        cuf,
        capex_cr_per_mw,
        om_lakh_per_mw_year,
        25,
        0.10,
        0.005
    )

    annual_generation_mwh = results["annual_generation_mwh"]
    lcoe = results["lcoe"]

    # --------------------------------------------------------
    # REGULATORY LOOKUPS
    # --------------------------------------------------------

    regulatory_context = (
        "Captive"
        if consumer_type == "Captive"
        else "Non-captive"
    )

    minimum_load_parameter = (
        "captive_minimum_load"
        if consumer_type == "Captive"
        else "geoa_minimum_load"
    )

    # Minimum load
    minimum_load = _regulatory_value(
        minimum_load_parameter,
        state=state,
        applicability=(
            "Captive"
            if consumer_type == "Captive"
            else "Non-captive Green Energy Open Access Consumer"
        )
    )

    # --------------------------------------------------------
    # RAJASTHAN BANKING REGIME
    # --------------------------------------------------------

    banking_regime = None
    banking_regime_applicability = None
    banking_ratio = None

    if consumer_type == "Captive":

        banking_ratio = capacity_mw / contract_demand_mw

        if banking_ratio <= 1.0:

            banking_regime = "Up to 100% of Contract Demand"
            banking_regime_applicability = (
                "RE captive power plant up to 100% of Contract Demand"
            )

        elif banking_ratio <= 2.0:

            banking_regime = "More than 100% to 200% of Contract Demand"
            banking_regime_applicability = (
                "RE captive power plant from 100% to 200% of Contract Demand"
            )

        else:

            banking_regime = "Above 200% of Contract Demand"
            banking_regime_applicability = None

    # --------------------------------------------------------
    # BANKING PROVISIONS
    # --------------------------------------------------------

    banking_lookup_applicability = (
        banking_regime_applicability
        if consumer_type == "Captive"
        else regulatory_context
    )

    # No banking regime is currently captured in the
    # regulatory database for captive RE capacity above
    # 200% of Contract Demand.
    if consumer_type == "Captive" and banking_regime_applicability is None:

        banking_eligibility = None
        banking_charge_rule = None
        banking_ceiling_energy = None
        banking_ceiling_consumption = None
        settlement_basis = None

    else:

        banking_eligibility = _regulatory_value(
            "banking_eligibility",
            state=state,
            applicability=banking_lookup_applicability,
            consumer_category=(
                "Captive"
                if consumer_type == "Captive"
                else "Non-captive"
            ),
            procurement_type=(
                "Captive"
                if consumer_type == "Captive"
                else "Open Access"
            )
        )

        banking_charge_rule = _regulatory_value(
            "banking_charge",
            state=state,
            applicability=banking_lookup_applicability,
            consumer_category=(
                "Captive"
                if consumer_type == "Captive"
                else "Non-captive"
            ),
            procurement_type=(
                "Captive"
                if consumer_type == "Captive"
                else "Open Access"
            )
        )

        banking_ceiling_energy = _regulatory_value(
            "banking_ceiling_energy_injected",
            state=state,
            applicability=banking_lookup_applicability,
            consumer_category=(
                "Captive"
                if consumer_type == "Captive"
                else "Non-captive"
            ),
            procurement_type=(
                "Captive"
                if consumer_type == "Captive"
                else "Open Access"
            )
        )

        banking_ceiling_consumption = _regulatory_value(
            "banking_ceiling_monthly_consumption",
            state=state,
            applicability=banking_lookup_applicability,
            consumer_category=(
                "Captive"
                if consumer_type == "Captive"
                else "Non-captive"
            ),
            procurement_type=(
                "Captive"
                if consumer_type == "Captive"
                else "Open Access"
            )
        )

        settlement_basis = _regulatory_value(
            "banking_settlement_basis",
            state=state,
            applicability=banking_lookup_applicability,
            consumer_category=(
                "Captive"
                if consumer_type == "Captive"
                else "Non-captive"
            ),
            procurement_type=(
                "Captive"
                if consumer_type == "Captive"
                else "Open Access"
        )
    )

    css_exemption = None
    as_exemption = None

    if consumer_type == "Captive":

        css_exemption = _regulatory_value(
            "css_captive_exemption",
            state=state,
            consumer_category="Captive",
            procurement_type="Captive"
        )

        as_exemption = _regulatory_value(
            "additional_surcharge_captive_exemption",
            state=state,
            consumer_category="Captive",
            procurement_type="Captive"
        )

    # --------------------------------------------------------
    # TARIFF LOOKUPS
    # --------------------------------------------------------

    tariff_date = "2026-04-01"

    # Convert UI "132 kV+" to database terminology
    tariff_voltage_level = (
        "132 kV and above"
        if voltage_level == "132 kV+"
        else voltage_level
    )

    wheeling_result = _tariff_lookup(
        "Wheeling Charge",
        state=state,
        voltage_level=tariff_voltage_level,
        effective_date=tariff_date
    )

    css_result = _tariff_lookup(
        "CSS Maximum",
        state=state,
        effective_date=tariff_date
    )

    additional_surcharge_result = _tariff_lookup(
        "Additional Surcharge",
        state=state,
        effective_date=tariff_date
    )

    transmission_loss_result = _tariff_lookup(
        "Transmission Loss",
        state=state,
        effective_date=tariff_date
    )

    wheeling_loss_result = _tariff_lookup(
        "Wheeling Loss",
        state=state,
        voltage_level=tariff_voltage_level,
        effective_date=tariff_date
    )

    acos_result = _tariff_lookup(
        "Average Cost of Supply",
        state=state,
        effective_date=tariff_date
    )

    standby_result = _tariff_lookup(
        "Standby Charge",
        state=state,
        effective_date=tariff_date
    )

    wheeling = _tariff_value(wheeling_result)
    css = _tariff_value(css_result)
    additional_surcharge = _tariff_value(
        additional_surcharge_result
    )

    transmission_loss = _tariff_value(
        transmission_loss_result
    )

    wheeling_loss = _tariff_value(
        wheeling_loss_result
    )

    acos = _tariff_value(acos_result)
    standby = _tariff_value(standby_result)

    # --------------------------------------------------------
    # LOSS-ADJUSTED ENERGY
    # --------------------------------------------------------

    transmission_loss_pct = (
        float(transmission_loss)
        if transmission_loss is not None
        else None
    )

    wheeling_loss_pct = (
        float(wheeling_loss)
        if wheeling_loss is not None
        else None
    )

    if (
        transmission_loss_pct is not None
        and wheeling_loss_pct is not None
    ):

        delivery_efficiency = (
            (1 - transmission_loss_pct / 100)
            * (1 - wheeling_loss_pct / 100)
        )

        loss_adjusted_lcoe = (
            lcoe / delivery_efficiency
            if delivery_efficiency > 0
            else None
        )

    else:

        delivery_efficiency = None
        loss_adjusted_lcoe = None

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Solar LCOE",
        f"₹{lcoe:.2f}/kWh"
    )

    col2.metric(
        "Annual Generation",
        f"{annual_generation_mwh:,.0f} MWh"
    )

    col3.metric(
        "Delivery Efficiency",
        (
            f"{delivery_efficiency * 100:.2f}%"
            if delivery_efficiency is not None
            else "N/A"
        )
    )

    col4.metric(
        "Loss-adjusted LCOE",
        (
            f"₹{loss_adjusted_lcoe:.2f}/kWh"
            if loss_adjusted_lcoe is not None
            else "N/A"
        )
    )

    # --------------------------------------------------------
    # REGULATORY STATUS
    # --------------------------------------------------------

    st.subheader("📋 Regulatory Applicability")

    regulatory_table = pd.DataFrame({
        "Provision": [
            "Minimum GEOA Load / Captive Load",
            "Banking Eligibility",
            "Banking Charge",
            "Banking Ceiling — Energy Injected",
            "Banking Ceiling — Monthly Consumption",
            "Banking Settlement Basis",
            "CSS Captive Exemption",
            "Additional Surcharge Captive Exemption",
        ],

        "Value": [
            minimum_load,
            banking_eligibility,
            banking_charge_rule,
            banking_ceiling_energy,
            banking_ceiling_consumption,
            settlement_basis,
            css_exemption,
            as_exemption,
        ],
    })

    st.dataframe(
        regulatory_table,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # TARIFF TABLE
    # --------------------------------------------------------

    st.subheader(
        "💰 Rajasthan Tariff Parameters — FY 2026–27"
    )

    tariff_rows = [
        ("Wheeling Charge", wheeling, "₹/kWh"),
        ("CSS Maximum", css, "₹/kWh"),
        ("Additional Surcharge", additional_surcharge, "₹/kWh"),
        ("Transmission Loss", transmission_loss, "%"),
        ("Wheeling Loss", wheeling_loss, "%"),
        ("Average Cost of Supply", acos, "₹/kWh"),
        ("Standby Charge", standby, "%"),
    ]

    tariff_table = pd.DataFrame(
        tariff_rows,
        columns=["Parameter", "Value", "Unit"]
    )

    tariff_table["Displayed Value"] = [
        _display_value(value, unit)
        for _, value, unit in tariff_rows
    ]

    st.dataframe(
        tariff_table[
            ["Parameter", "Displayed Value", "Unit"]
        ],
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # RAJASTHAN MONTHLY BANKING ANALYSIS
    # --------------------------------------------------------

    st.divider()

    st.subheader("🔋 Rajasthan Monthly Banking Analysis")

    st.caption(
        "Monthly energy-flow calculation using the selected Rajasthan "
        "banking regime and the regulatory parameters retrieved above."
    )

    # --------------------------------------------------------
    # MONTHLY PROFILES
    # --------------------------------------------------------

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    demand_shares_v04 = [
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

    solar_shares_v04 = [
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
    # MONTHLY INPUT ENERGY
    # --------------------------------------------------------

    monthly_df = pd.DataFrame({
        "Month": months,
        "Demand Share": demand_shares_v04,
        "Solar Share": solar_shares_v04
    })

    monthly_df["Demand (MWh)"] = (
        annual_consumption_mwh
        * monthly_df["Demand Share"]
    )

    monthly_df["Solar Generation (MWh)"] = (
        annual_generation_mwh
        * monthly_df["Solar Share"]
    )

    # --------------------------------------------------------
    # DIRECT RENEWABLE CONSUMPTION
    # --------------------------------------------------------

    monthly_df["Direct Renewable Consumption (MWh)"] = (
        monthly_df[
            [
                "Demand (MWh)",
                "Solar Generation (MWh)"
            ]
        ].min(axis=1)
    )

    # --------------------------------------------------------
    # SURPLUS AND SHORTFALL
    # --------------------------------------------------------

    monthly_df["Solar Surplus (MWh)"] = (
        monthly_df["Solar Generation (MWh)"]
        - monthly_df["Direct Renewable Consumption (MWh)"]
    )

    monthly_df["Grid Shortfall Before Banking (MWh)"] = (
        monthly_df["Demand (MWh)"]
        - monthly_df["Direct Renewable Consumption (MWh)"]
    )

    # --------------------------------------------------------
    # BANKING CALCULATION
    # --------------------------------------------------------

    monthly_df["Banking Ceiling (MWh)"] = 0.0
    monthly_df["Gross Banked Energy (MWh)"] = 0.0
    monthly_df["Banking Charge Energy (MWh)"] = 0.0
    monthly_df["Bank Withdrawal (MWh)"] = 0.0
    monthly_df["Grid Requirement After Banking (MWh)"] = (
        monthly_df["Grid Shortfall Before Banking (MWh)"]
    )
    monthly_df["Ending Bank Balance (MWh)"] = 0.0

    banking_charge_fraction = 0.0

    if (
        consumer_type == "Captive"
        and banking_regime_applicability is not None
        and banking_eligibility == "Yes"
    ):

        try:
            banking_charge_fraction = (
                float(banking_charge_rule) / 100
            )
        except Exception:
            banking_charge_fraction = 0.0

        # ----------------------------------------------------
        # REGIME 1: UP TO 100% OF CONTRACT DEMAND
        # ----------------------------------------------------

        if banking_regime == "Up to 100% of Contract Demand":

            energy_ceiling_pct = (
                float(banking_ceiling_energy)
                if banking_ceiling_energy is not None
                else 0.0
            )

            consumption_ceiling_pct = (
                float(banking_ceiling_consumption)
                if banking_ceiling_consumption is not None
                else 0.0
            )

            bank_balance = 0.0

            for i in range(len(monthly_df)):

                demand = monthly_df.loc[i, "Demand (MWh)"]
                surplus = monthly_df.loc[i, "Solar Surplus (MWh)"]
                shortfall = monthly_df.loc[
                    i,
                    "Grid Shortfall Before Banking (MWh)"
                ]

                # Rajasthan ceiling:
                # higher of 25% of monthly injected energy
                # or 30% of monthly consumption.
                ceiling_energy = (
                    surplus * energy_ceiling_pct / 100
                )

                ceiling_consumption = (
                    demand * consumption_ceiling_pct / 100
                )

                banking_ceiling = max(
                    ceiling_energy,
                    ceiling_consumption
                )

                gross_banked = min(
                    surplus,
                    banking_ceiling
                )

                bank_balance += gross_banked

                # 8% charge is deducted from banked energy
                # when energy is withdrawn.
                usable_balance = (
                    bank_balance
                    * (1 - banking_charge_fraction)
                )

                withdrawal = min(
                    shortfall,
                    usable_balance
                )

                gross_energy_used = (
                    withdrawal / (1 - banking_charge_fraction)
                    if (
                        withdrawal > 0
                        and banking_charge_fraction < 1
                    )
                    else 0.0
                )

                gross_energy_used = min(
                    gross_energy_used,
                    bank_balance
                )

                banking_charge_energy = (
                    gross_energy_used
                    - withdrawal
                )

                bank_balance -= gross_energy_used

                grid_after_banking = (
                    shortfall - withdrawal
                )

                monthly_df.loc[i, "Banking Ceiling (MWh)"] = (
                    banking_ceiling
                )

                monthly_df.loc[
                    i,
                    "Gross Banked Energy (MWh)"
                ] = gross_banked

                monthly_df.loc[
                    i,
                    "Banking Charge Energy (MWh)"
                ] = banking_charge_energy

                monthly_df.loc[
                    i,
                    "Bank Withdrawal (MWh)"
                ] = withdrawal

                monthly_df.loc[
                    i,
                    "Grid Requirement After Banking (MWh)"
                ] = grid_after_banking

                monthly_df.loc[
                    i,
                    "Ending Bank Balance (MWh)"
                ] = bank_balance

            # Annual settlement:
            # remaining banked energy lapses at year-end.
            annual_lapsed_energy = bank_balance

        # ----------------------------------------------------
        # REGIME 2: >100% TO 200%
        # ----------------------------------------------------

        elif (
            banking_regime
            == "More than 100% to 200% of Contract Demand"
        ):

            consumption_ceiling_pct = (
                float(banking_ceiling_consumption)
                if banking_ceiling_consumption is not None
                else 0.0
            )

            # Billing-cycle settlement:
            # each month is treated as an independent billing cycle.
            for i in range(len(monthly_df)):

                demand = monthly_df.loc[i, "Demand (MWh)"]
                surplus = monthly_df.loc[i, "Solar Surplus (MWh)"]
                shortfall = monthly_df.loc[
                    i,
                    "Grid Shortfall Before Banking (MWh)"
                ]

                banking_ceiling = (
                    demand
                    * consumption_ceiling_pct
                    / 100
                )

                gross_banked = min(
                    surplus,
                    banking_ceiling
                )

                usable_banked = (
                    gross_banked
                    * (1 - banking_charge_fraction)
                )

                withdrawal = min(
                    shortfall,
                    usable_banked
                )

                banking_charge_energy = (
                    withdrawal
                    * banking_charge_fraction
                    / (1 - banking_charge_fraction)
                    if (
                        withdrawal > 0
                        and banking_charge_fraction < 1
                    )
                    else 0.0
                )

                grid_after_banking = (
                    shortfall - withdrawal
                )

                ending_balance = max(
                    gross_banked
                    - withdrawal
                    - banking_charge_energy,
                    0.0
                )

                # Billing-cycle balance lapses at the end
                # of each cycle.
                monthly_df.loc[
                    i,
                    "Banking Ceiling (MWh)"
                ] = banking_ceiling

                monthly_df.loc[
                    i,
                    "Gross Banked Energy (MWh)"
                ] = gross_banked

                monthly_df.loc[
                    i,
                    "Banking Charge Energy (MWh)"
                ] = banking_charge_energy

                monthly_df.loc[
                    i,
                    "Bank Withdrawal (MWh)"
                ] = withdrawal

                monthly_df.loc[
                    i,
                    "Grid Requirement After Banking (MWh)"
                ] = grid_after_banking

                monthly_df.loc[
                    i,
                    "Ending Bank Balance (MWh)"
                ] = ending_balance

            annual_lapsed_energy = (
                monthly_df["Ending Bank Balance (MWh)"].sum()
            )

        else:

            annual_lapsed_energy = 0.0

    else:

        annual_lapsed_energy = 0.0

    # --------------------------------------------------------
    # DISPLAY BANKING STATUS
    # --------------------------------------------------------

    if consumer_type != "Captive":

        st.info(
            "Rajasthan banking provisions currently captured in the "
            "regulatory database apply to captive consumption. "
            "No banking calculation is applied to the selected "
            "Non-Captive case."
        )

    elif banking_regime == "Above 200% of Contract Demand":

        st.warning(
            "The selected renewable capacity is above 200% of "
            "Contract Demand. No applicable Rajasthan banking regime "
            "is currently captured in the regulatory database. "
            "Banking is therefore not calculated."
        )

    elif banking_regime is not None:

        st.success(
            f"Banking regime applied: **{banking_regime}** | "
            f"Settlement: **{settlement_basis}** | "
            f"Banking charge: **{banking_charge_rule}%**"
        )

    else:

        st.warning(
            "No applicable banking regime is available for the "
            "selected configuration."
        )

    # --------------------------------------------------------
    # MONTHLY BANKING TABLE
    # --------------------------------------------------------

    display_columns = [
        "Month",
        "Demand (MWh)",
        "Solar Generation (MWh)",
        "Direct Renewable Consumption (MWh)",
        "Solar Surplus (MWh)",
        "Grid Shortfall Before Banking (MWh)",
        "Banking Ceiling (MWh)",
        "Gross Banked Energy (MWh)",
        "Banking Charge Energy (MWh)",
        "Bank Withdrawal (MWh)",
        "Grid Requirement After Banking (MWh)",
        "Ending Bank Balance (MWh)"
    ]

    st.dataframe(
        monthly_df[display_columns].round(2),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # MONTHLY BANKING KPIs
    # --------------------------------------------------------

    total_demand_v04 = monthly_df["Demand (MWh)"].sum()
    total_solar_v04 = monthly_df["Solar Generation (MWh)"].sum()
    total_direct_v04 = monthly_df[
        "Direct Renewable Consumption (MWh)"
    ].sum()
    total_surplus_v04 = monthly_df[
        "Solar Surplus (MWh)"
    ].sum()
    total_withdrawal_v04 = monthly_df[
        "Bank Withdrawal (MWh)"
    ].sum()
    total_grid_after_banking_v04 = monthly_df[
        "Grid Requirement After Banking (MWh)"
    ].sum()
    total_banking_charge_v04 = monthly_df[
        "Banking Charge Energy (MWh)"
    ].sum()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Annual Demand",
        f"{total_demand_v04:,.0f} MWh"
    )

    k2.metric(
        "Solar Generation",
        f"{total_solar_v04:,.0f} MWh"
    )

    k3.metric(
        "Bank Withdrawal",
        f"{total_withdrawal_v04:,.0f} MWh"
    )

    k4.metric(
        "Banking Charge",
        f"{total_banking_charge_v04:,.0f} MWh"
    )

    # --------------------------------------------------------
    # BANKING SETTLEMENT SUMMARY
    # --------------------------------------------------------

    st.subheader("📊 Banking Settlement Summary")

    settlement_summary = pd.DataFrame({
        "Metric": [
            "Total Solar Generation",
            "Direct Renewable Consumption",
            "Solar Surplus",
            "Bank Withdrawal",
            "Grid Requirement After Banking",
            "Banking Charge Energy",
            "Lapsed / Unused Banked Energy"
        ],
        "MWh": [
            total_solar_v04,
            total_direct_v04,
            total_surplus_v04,
            total_withdrawal_v04,
            total_grid_after_banking_v04,
            total_banking_charge_v04,
            annual_lapsed_energy
        ]
    })

    st.dataframe(
        settlement_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # COST BUILD-UP
    # --------------------------------------------------------

    st.subheader(
        "🔌 Renewable Open Access Cost Build-up"
    )

    # --------------------------------------------------------
    # Determine applicable charges
    # --------------------------------------------------------

    if consumer_type == "Captive":

        # Captive consumers are exempt from CSS and
        # Additional Surcharge under the validated
        # regulatory database provisions.
        applicable_wheeling = wheeling
        applicable_css = 0.0
        applicable_additional_surcharge = 0.0

        css_status = "Exempt — Captive"
        as_status = "Exempt — Captive"

    else:

        # Non-captive Open Access
        applicable_wheeling = wheeling
        applicable_css = css
        applicable_additional_surcharge = additional_surcharge

        css_status = "Applicable"
        as_status = "Applicable"


    # --------------------------------------------------------
    # Cost components
    # --------------------------------------------------------

    cost_rows = [
        ("Solar LCOE", lcoe),
        ("Wheeling Charge", applicable_wheeling),
        ("CSS", applicable_css),
        ("Additional Surcharge", applicable_additional_surcharge),
    ]

    cost_df = pd.DataFrame(
        cost_rows,
        columns=["Component", "₹/kWh"]
    )


    # --------------------------------------------------------
    # Add explanatory status
    # --------------------------------------------------------

    cost_status_df = pd.DataFrame({
        "Component": [
            "CSS",
            "Additional Surcharge",
        ],
        "Regulatory Treatment": [
            css_status,
            as_status,
        ],
    })

    st.dataframe(
        cost_df.round(3),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Regulatory treatment of captive exemptions:"
    )

    st.dataframe(
        cost_status_df,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Calculate indicative delivered cost
    # --------------------------------------------------------

    if (
        applicable_wheeling is not None
        and loss_adjusted_lcoe is not None
    ):

        regulatory_charges = (
            applicable_wheeling
            + applicable_css
            + applicable_additional_surcharge
        )

        indicative_cost = (
            loss_adjusted_lcoe
            + regulatory_charges
        )

        st.metric(
            "Indicative Delivered Cost — excluding transmission",
            f"₹{indicative_cost:.3f}/kWh"
        )

        st.info(
            "This is an indicative delivered cost excluding "
            "transmission charges. For captive procurement, CSS "
            "and Additional Surcharge are excluded based on the "
            "validated captive exemption provisions."
            if consumer_type == "Captive"
            else
            "This is an indicative delivered cost excluding "
            "transmission charges."
        )

        st.warning(
            "Transmission charge is not numerically linked in "
            "the current tariff database. Therefore, this is "
            "not a final all-in OA cost."
        )

    else:

        st.warning(
            "A complete delivered-cost calculation cannot be "
            "produced because one or more required values "
            "are not available."
        )
    # --------------------------------------------------------
    # SOURCE TRACEABILITY
    # --------------------------------------------------------

    st.subheader("🔎 Source & Traceability")

    source_results = [
        ("Wheeling Charge", wheeling_result),
        ("CSS Maximum", css_result),
        ("Additional Surcharge", additional_surcharge_result),
        ("Transmission Loss", transmission_loss_result),
        ("Wheeling Loss", wheeling_loss_result),
        ("Average Cost of Supply", acos_result),
        ("Standby Charge", standby_result),
    ]

    source_rows = []

    for label, result in source_results:

        source_rows.append({
            "Parameter": label,
            "Source": _tariff_source_text(result)
        })

    st.dataframe(
        pd.DataFrame(source_rows),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # MODEL NOTES
    # --------------------------------------------------------

    st.subheader("⚠️ Model Notes")

    st.markdown(
        """
        - Version 0.4 separates **regulatory rules** from **tariff values**.
        - Regulatory provisions are retrieved from the Rajasthan regulatory database.
        - Tariff values are retrieved from the Rajasthan tariff database.
        - Missing numerical values are **not treated as zero**.
        - Voltage-specific wheeling charges and losses are linked to the selected voltage level.
        - Transmission charge is identified as tariff-dependent but is not numerically linked in the present database.
        - Banking settlement and monthly banking mechanics will be integrated into the Version 0.4 monthly model after this regulatory layer is validated.
        """
    )

    st.download_button(
        "⬇️ Download Rajasthan Tariff Summary",
        tariff_table.to_csv(index=False),
        "version_04_rajasthan_tariff_summary.csv",
        "text/csv",
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
        "Version 0.3 — Monthly Analysis",
        "Version 0.4 — Rajasthan Regulatory"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "India RE Power Procurement Tool"
)

st.sidebar.caption(
    "Prototype: Versions 0.1–0.4"
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

elif page == "Version 0.4 — Rajasthan Regulatory":

    version_04()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Prototype analytical tool | Versions 0.1, 0.2, 0.3 and 0.4"
)
