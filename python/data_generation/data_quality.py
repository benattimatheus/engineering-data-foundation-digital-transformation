# python/data_generation/data_quality.py

import random

import numpy as np
import pandas as pd

from data_generation.config import (
    MISSING_OWNER_RATE,
    MISSING_EQUIPMENT_RATE,
    MISSING_DISCIPLINE_RATE,
    MISSING_DOCUMENT_TYPE_RATE,
    DUPLICATE_DOCUMENT_ID_RATE,
    INVALID_STATUS_RATE,
    INVALID_DATE_RATE,
    MISSING_APPROVAL_DATE_RATE,
    INCONSISTENT_REVISION_RATE,
    INVALID_EQUIPMENT_CRITICALITY_RATE,
    MISSING_PROJECT_PHASE_RATE,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def set_random_null(
    dataframe: pd.DataFrame,
    column: str,
    rate: float,
) -> None:
    """
    Randomly sets values in a column to null.

    This simulates missing metadata issues commonly found
    in manually maintained engineering trackers.
    """

    selected_index = dataframe.sample(
        frac=rate,
        random_state=random.randint(1, 10000),
    ).index

    dataframe.loc[selected_index, column] = pd.NA


# ============================================================
# DATA QUALITY ISSUE INJECTION
# ============================================================

def inject_missing_metadata_issues(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects missing metadata issues into the fact table.
    """

    set_random_null(
        dataframe=fact_engineering_deliverables,
        column="responsible_engineer_id",
        rate=MISSING_OWNER_RATE,
    )

    set_random_null(
        dataframe=fact_engineering_deliverables,
        column="equipment_id",
        rate=MISSING_EQUIPMENT_RATE,
    )

    set_random_null(
        dataframe=fact_engineering_deliverables,
        column="discipline_id",
        rate=MISSING_DISCIPLINE_RATE,
    )

    set_random_null(
        dataframe=fact_engineering_deliverables,
        column="document_type_id",
        rate=MISSING_DOCUMENT_TYPE_RATE,
    )


def inject_duplicate_document_ids(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects duplicate document IDs into the fact table.

    This simulates inconsistent document control practices.
    """

    duplicate_index = fact_engineering_deliverables.sample(
        frac=DUPLICATE_DOCUMENT_ID_RATE,
        random_state=101,
    ).index

    source_document_ids = (
        fact_engineering_deliverables
        .drop(index=duplicate_index)
        .sample(
            n=len(duplicate_index),
            random_state=102,
        )["document_id"]
        .values
    )

    fact_engineering_deliverables.loc[
        duplicate_index,
        "document_id",
    ] = source_document_ids


def inject_invalid_status_issues(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects invalid status IDs into the fact table.
    """

    invalid_status_index = fact_engineering_deliverables.sample(
        frac=INVALID_STATUS_RATE,
        random_state=103,
    ).index

    fact_engineering_deliverables.loc[
        invalid_status_index,
        "status_id",
    ] = "STAT-999"


def inject_invalid_date_issues(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects invalid date logic into the fact table.

    Example:
    actual submission date happens before the planned submission date,
    but the planned date is later overwritten in an inconsistent way.
    """

    invalid_date_index = fact_engineering_deliverables.sample(
        frac=INVALID_DATE_RATE,
        random_state=104,
    ).index

    fact_engineering_deliverables.loc[
        invalid_date_index,
        "actual_submission_date",
    ] = (
        fact_engineering_deliverables.loc[
            invalid_date_index,
            "planned_submission_date",
        ]
        - pd.to_timedelta(
            np.random.randint(
                10,
                35,
                len(invalid_date_index),
            ),
            unit="D",
        )
    )

    fact_engineering_deliverables.loc[
        invalid_date_index,
        "planned_submission_date",
    ] = (
        fact_engineering_deliverables.loc[
            invalid_date_index,
            "actual_submission_date",
        ]
        + pd.to_timedelta(
            np.random.randint(
                40,
                70,
                len(invalid_date_index),
            ),
            unit="D",
        )
    )


def inject_workflow_issues(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects workflow-related issues.

    Example:
    approved deliverables without an actual approval date.
    """

    approved_records = fact_engineering_deliverables[
        fact_engineering_deliverables["status_id"] == "STAT-004"
    ]

    if approved_records.empty:
        return

    approved_index = approved_records.sample(
        frac=MISSING_APPROVAL_DATE_RATE,
        random_state=105,
    ).index

    fact_engineering_deliverables.loc[
        approved_index,
        "actual_approval_date",
    ] = pd.NaT


def inject_revision_issues(
    fact_engineering_deliverables: pd.DataFrame,
) -> None:
    """
    Injects inconsistent revision numbers.
    """

    bad_revision_index = fact_engineering_deliverables.sample(
        frac=INCONSISTENT_REVISION_RATE,
        random_state=106,
    ).index

    fact_engineering_deliverables.loc[
        bad_revision_index,
        "revision_number",
    ] = np.random.choice(
        [-1, 9, 15],
        len(bad_revision_index),
    )


def inject_dimension_quality_issues(
    dim_equipment: pd.DataFrame,
    dim_project: pd.DataFrame,
) -> None:
    """
    Injects quality issues into dimensions.

    Examples:
    - Undefined equipment criticality
    - Missing project phase
    """

    bad_criticality_index = dim_equipment.sample(
        frac=INVALID_EQUIPMENT_CRITICALITY_RATE,
        random_state=107,
    ).index

    dim_equipment.loc[
        bad_criticality_index,
        "criticality",
    ] = "Undefined"

    missing_phase_index = dim_project.sample(
        frac=MISSING_PROJECT_PHASE_RATE,
        random_state=108,
    ).index

    dim_project.loc[
        missing_phase_index,
        "project_phase",
    ] = pd.NA


def inject_data_quality_issues(
    fact_engineering_deliverables: pd.DataFrame,
    dim_equipment: pd.DataFrame,
    dim_project: pd.DataFrame,
) -> None:
    """
    Runs all data quality issue injections.

    This function modifies the dataframes in place.
    """

    inject_missing_metadata_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_duplicate_document_ids(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_invalid_status_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_invalid_date_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_workflow_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_revision_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
    )

    inject_dimension_quality_issues(
        dim_equipment=dim_equipment,
        dim_project=dim_project,
    )