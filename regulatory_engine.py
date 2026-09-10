from pathlib import Path
import pandas as pd


class RegulatoryEngine:
    """
    State-neutral regulatory parameter retrieval engine.

    Supports:
    1. Regulatory rules database
    2. Tariff / charge database
    3. Source traceability
    4. State and applicability filtering
    5. Voltage-level filtering
    6. Effective-date filtering
    """

    def __init__(
        self,
        database_path,
        tariff_database_path=None
    ):

        # ----------------------------------------------------
        # REGULATORY DATABASE
        # ----------------------------------------------------

        self.database_path = Path(database_path)

        if not self.database_path.exists():
            raise FileNotFoundError(
                f"Regulatory database not found: "
                f"{self.database_path}"
            )

        self.db = pd.read_csv(
            self.database_path
        )

        # ----------------------------------------------------
        # TARIFF DATABASE
        # ----------------------------------------------------

        self.tariff_database_path = None
        self.tariff_db = pd.DataFrame()

        if tariff_database_path is not None:

            self.tariff_database_path = Path(
                tariff_database_path
            )

            if not self.tariff_database_path.exists():
                raise FileNotFoundError(
                    f"Tariff database not found: "
                    f"{self.tariff_database_path}"
                )

            self.tariff_db = pd.read_csv(
                self.tariff_database_path
            )

    # ========================================================
    # HELPER FUNCTIONS
    # ========================================================

    @staticmethod
    def _exact_match(series, value):

        return (
            series
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            == str(value).strip().lower()
        )

    @staticmethod
    def _contains_match(series, value):

        return (
            series
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                str(value).lower(),
                regex=False
            )
        )

    # ========================================================
    # REGULATORY DATABASE
    # ========================================================

    def filter(
        self,
        state=None,
        parameter_id=None,
        parameter=None,
        consumer_category=None,
        applicability=None,
        procurement_type=None
    ):

        result = self.db.copy()

        if state is not None:
            result = result[
                self._exact_match(
                    result["State"],
                    state
                )
            ]

        if parameter_id is not None:
            result = result[
                self._exact_match(
                    result["Parameter ID"],
                    parameter_id
                )
            ]

        if parameter is not None:
            result = result[
                self._exact_match(
                    result["Parameter"],
                    parameter
                )
            ]

        if consumer_category is not None:
            result = result[
                self._contains_match(
                    result["Consumer Category"],
                    consumer_category
                )
            ]

        if applicability is not None:
            result = result[
                self._contains_match(
                    result["Applicability"],
                    applicability
                )
            ]

        if procurement_type is not None:
            result = result[
                self._contains_match(
                    result["Procurement Type"],
                    procurement_type
                )
            ]

        return result.reset_index(drop=True)

    # ========================================================
    # REGULATORY PARAMETER
    # ========================================================

    def get_parameter(
        self,
        state,
        parameter_id=None,
        parameter=None,
        consumer_category=None,
        applicability=None,
        procurement_type=None
    ):

        if parameter_id is None and parameter is None:
            raise ValueError(
                "Provide either parameter_id or parameter."
            )

        return self.filter(
            state=state,
            parameter_id=parameter_id,
            parameter=parameter,
            consumer_category=consumer_category,
            applicability=applicability,
            procurement_type=procurement_type
        )

    # ========================================================
    # REGULATORY SOURCE
    # ========================================================

    def get_source(
        self,
        state,
        parameter_id=None,
        parameter=None,
        consumer_category=None,
        applicability=None,
        procurement_type=None
    ):

        result = self.get_parameter(
            state=state,
            parameter_id=parameter_id,
            parameter=parameter,
            consumer_category=consumer_category,
            applicability=applicability,
            procurement_type=procurement_type
        )

        if result.empty:
            return result

        source_columns = [
            "State",
            "Regulator",
            "Parameter ID",
            "Parameter",
            "Value",
            "Unit",
            "Applicability",
            "Consumer Category",
            "Effective From",
            "Effective To",
            "Document",
            "Regulation",
            "Clause",
            "Page",
            "Source URL",
            "Status",
            "Notes"
        ]

        available_columns = [
            col for col in source_columns
            if col in result.columns
        ]

        return result[available_columns]

    # ========================================================
    # AVAILABLE PARAMETERS
    # ========================================================

    def available_parameters(
        self,
        state=None
    ):

        result = self.db.copy()

        if state is not None:
            result = result[
                self._exact_match(
                    result["State"],
                    state
                )
            ]

        return (
            result[
                ["Parameter ID", "Parameter"]
            ]
            .drop_duplicates()
            .sort_values("Parameter ID")
            .reset_index(drop=True)
        )

    # ========================================================
    # AVAILABLE STATES
    # ========================================================

    def available_states(self):

        return sorted(
            self.db["State"]
            .dropna()
            .unique()
            .tolist()
        )

    # ========================================================
    # TARIFF DATABASE
    # ========================================================

    def filter_tariff(
        self,
        state=None,
        parameter=None,
        consumer_category=None,
        voltage_level=None,
        discom=None,
        procurement_type=None,
        technology=None,
        applicability=None,
        effective_date=None
    ):
        """
        Filter tariff / charge records.
        """

        if self.tariff_db.empty:
            return pd.DataFrame()

        result = self.tariff_db.copy()

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        if state is not None:
            result = result[
                self._exact_match(
                    result["State"],
                    state
                )
            ]

        # ----------------------------------------------------
        # PARAMETER
        # ----------------------------------------------------

        if parameter is not None:
            result = result[
                self._exact_match(
                    result["Parameter"],
                    parameter
                )
            ]

        # ----------------------------------------------------
        # CONSUMER CATEGORY
        # ----------------------------------------------------

        if consumer_category is not None:
            result = result[
                self._contains_match(
                    result["Consumer Category"],
                    consumer_category
                )
            ]

        # ----------------------------------------------------
        # VOLTAGE LEVEL
        # ----------------------------------------------------

        if voltage_level is not None:
            result = result[
                self._contains_match(
                    result["Voltage Level"],
                    voltage_level
                )
            ]

        # ----------------------------------------------------
        # DISCOM
        # ----------------------------------------------------

        if discom is not None:
            result = result[
                self._contains_match(
                    result["DISCOM"],
                    discom
                )
            ]

        # ----------------------------------------------------
        # PROCUREMENT TYPE
        # ----------------------------------------------------

        if procurement_type is not None:
            result = result[
                self._contains_match(
                    result["Procurement Type"],
                    procurement_type
                )
            ]

        # ----------------------------------------------------
        # TECHNOLOGY
        # ----------------------------------------------------

        if technology is not None:
            result = result[
                self._contains_match(
                    result["Technology"],
                    technology
                )
            ]

        # ----------------------------------------------------
        # APPLICABILITY
        # ----------------------------------------------------

        if applicability is not None:
            result = result[
                self._contains_match(
                    result["Applicability"],
                    applicability
                )
            ]

        # ----------------------------------------------------
        # EFFECTIVE DATE
        # ----------------------------------------------------

        if effective_date is not None:

            target_date = pd.to_datetime(
                effective_date,
                errors="coerce"
            )

            if pd.notna(target_date):

                if "Effective From" in result.columns:

                    effective_from = pd.to_datetime(
                        result["Effective From"],
                        errors="coerce"
                    )

                    result = result[
                        effective_from.isna()
                        | (
                            effective_from
                            <= target_date
                        )
                    ]

                if "Effective To" in result.columns:

                    effective_to = pd.to_datetime(
                        result["Effective To"],
                        errors="coerce"
                    )

                    result = result[
                        effective_to.isna()
                        | (
                            effective_to
                            >= target_date
                        )
                    ]

        return result.reset_index(drop=True)

    # ========================================================
    # TARIFF VALUE
    # ========================================================

    def get_tariff_value(
        self,
        state,
        parameter,
        consumer_category=None,
        voltage_level=None,
        discom=None,
        procurement_type=None,
        technology=None,
        applicability=None,
        effective_date=None
    ):

        return self.filter_tariff(
            state=state,
            parameter=parameter,
            consumer_category=consumer_category,
            voltage_level=voltage_level,
            discom=discom,
            procurement_type=procurement_type,
            technology=technology,
            applicability=applicability,
            effective_date=effective_date
        )

    # ========================================================
    # TARIFF SOURCE
    # ========================================================

    def get_tariff_source(
        self,
        state,
        parameter,
        consumer_category=None,
        voltage_level=None,
        effective_date=None
    ):

        result = self.get_tariff_value(
            state=state,
            parameter=parameter,
            consumer_category=consumer_category,
            voltage_level=voltage_level,
            effective_date=effective_date
        )

        if result.empty:
            return result

        source_columns = [
            "State",
            "Regulator",
            "Parameter",
            "Value",
            "Unit",
            "Applicability",
            "Consumer Category",
            "Voltage Level",
            "DISCOM",
            "Procurement Type",
            "Technology",
            "Effective From",
            "Effective To",
            "Tariff Year",
            "Document",
            "Regulation",
            "Clause",
            "Page",
            "Source URL",
            "Status",
            "Notes"
        ]

        available_columns = [
            col for col in source_columns
            if col in result.columns
        ]

        return result[available_columns]

    # ========================================================
    # SINGLE TARIFF VALUE
    # ========================================================

    def get_single_tariff_value(
        self,
        state,
        parameter,
        consumer_category=None,
        voltage_level=None,
        discom=None,
        procurement_type=None,
        technology=None,
        applicability=None,
        effective_date=None
    ):
        """
        Return the first applicable tariff record.

        Missing tariff values return None.
        They are NOT treated as zero.
        """

        result = self.get_tariff_value(
            state=state,
            parameter=parameter,
            consumer_category=consumer_category,
            voltage_level=voltage_level,
            discom=discom,
            procurement_type=procurement_type,
            technology=technology,
            applicability=applicability,
            effective_date=effective_date
        )

        if result.empty:

            return {
                "found": False,
                "value": None,
                "unit": None,
                "record": None,
                "message": (
                    f"No applicable tariff record found "
                    f"for '{parameter}' in {state}."
                )
            }

        row = result.iloc[0]

        return {
            "found": True,
            "value": row.get("Value"),
            "unit": row.get("Unit"),
            "record": row.to_dict(),
            "message": "Applicable tariff record found."
        }


# ============================================================
# USER-FACING REGULATORY LOOKUP
# ============================================================

def lookup_parameter(
    engine,
    state,
    parameter_id=None,
    parameter=None,
    consumer_category=None,
    applicability=None,
    procurement_type=None
):

    result = engine.get_parameter(
        state=state,
        parameter_id=parameter_id,
        parameter=parameter,
        consumer_category=consumer_category,
        applicability=applicability,
        procurement_type=procurement_type
    )

    if result.empty:

        return {
            "found": False,
            "count": 0,
            "records": [],
            "message": (
                f"No regulatory parameter found for "
                f"'{parameter_id or parameter}' in {state}."
            )
        }

    records = []

    for _, row in result.iterrows():

        records.append({
            "state": row.get("State"),
            "regulator": row.get("Regulator"),
            "parameter_id": row.get("Parameter ID"),
            "parameter": row.get("Parameter"),
            "value": row.get("Value"),
            "unit": row.get("Unit"),
            "applicability": row.get("Applicability"),
            "consumer_category": row.get("Consumer Category"),
            "voltage_level": row.get("Voltage Level"),
            "discom": row.get("DISCOM"),
            "procurement_type": row.get("Procurement Type"),
            "technology": row.get("Technology"),
            "effective_from": row.get("Effective From"),
            "effective_to": row.get("Effective To"),
            "document": row.get("Document"),
            "regulation": row.get("Regulation"),
            "clause": row.get("Clause"),
            "page": row.get("Page"),
            "source_url": row.get("Source URL"),
            "status": row.get("Status"),
            "notes": row.get("Notes")
        })

    return {
        "found": True,
        "count": len(records),
        "records": records
    }


# ============================================================
# USER-FACING TARIFF LOOKUP
# ============================================================

def lookup_tariff(
    engine,
    state,
    parameter,
    consumer_category=None,
    voltage_level=None,
    effective_date=None,
    applicability=None
):

    return engine.get_single_tariff_value(
        state=state,
        parameter=parameter,
        consumer_category=consumer_category,
        voltage_level=voltage_level,
        effective_date=effective_date,
        applicability=applicability
    )