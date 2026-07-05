import random

import numpy as np
import pandas as pd

from data_generation.config import (
    N_DELIVERABLES,
    DELIVERABLE_START_DATE,
    DELIVERABLE_PLANNING_DAYS,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_document_type_name(document_type_name: str) -> str:
    """
    Converts a document type name into a clean text format
    to be used inside the synthetic document ID.
    """

    return (
        document_type_name
        .replace("&", "AND")
        .replace(" ", "-")
        .replace("/", "-")
        .upper()
    )


def get_status_name(status_id: str, dim_status: pd.DataFrame) -> str:
    """
    Returns the status name based on the status ID.
    """

    return dim_status.loc[
        dim_status["status_id"] == status_id,
        "status_name",
    ].iloc[0]


def get_document_type_name(
    document_type_id: str,
    dim_document_type: pd.DataFrame,
) -> str:
    """
    Returns the document type name based on the document type ID.
    """

    return dim_document_type.loc[
        dim_document_type["document_type_id"] == document_type_id,
        "document_type_name",
    ].iloc[0]


def get_engineer_for_discipline(
    discipline_id: str,
    dim_engineer: pd.DataFrame,
) -> str:
    """
    Selects an engineer from the same discipline when possible.
    If no engineer exists for that discipline, selects any engineer.
    """

    possible_engineers = dim_engineer.loc[
        dim_engineer["discipline_id"] == discipline_id,
        "responsible_engineer_id",
    ].tolist()

    if possible_engineers:
        return random.choice(possible_engineers)

    return random.choice(
        dim_engineer["responsible_engineer_id"].tolist()
    )


def generate_dates_for_status(
    status_name: str,
    planned_submission_date: pd.Timestamp,
) -> tuple[pd.Timestamp | pd.NaT, pd.Timestamp | pd.NaT]:
    """
    Generates actual submission and approval dates according to the workflow status.
    """

    if status_name in ["Approved", "Rejected"]:
        actual_submission_date = planned_submission_date + pd.to_timedelta(
            random.randint(-5, 25),
            unit="D",
        )

        actual_approval_date = actual_submission_date + pd.to_timedelta(
            random.randint(2, 30),
            unit="D",
        )

    elif status_name == "Under Review":
        actual_submission_date = planned_submission_date + pd.to_timedelta(
            random.randint(-3, 20),
            unit="D",
        )

        actual_approval_date = pd.NaT

    elif status_name == "Delayed":
        if random.random() < 0.55:
            actual_submission_date = pd.NaT
        else:
            actual_submission_date = planned_submission_date + pd.to_timedelta(
                random.randint(10, 45),
                unit="D",
            )

        actual_approval_date = pd.NaT

    elif status_name == "Cancelled":
        actual_submission_date = pd.NaT
        actual_approval_date = pd.NaT

    else:
        if random.random() < 0.75:
            actual_submission_date = pd.NaT
        else:
            actual_submission_date = planned_submission_date + pd.to_timedelta(
                random.randint(-2, 10),
                unit="D",
            )

        actual_approval_date = pd.NaT

    return actual_submission_date, actual_approval_date


# ============================================================
# FACT TABLE
# ============================================================

def create_fact_engineering_deliverables(
    dim_project: pd.DataFrame,
    dim_discipline: pd.DataFrame,
    dim_document_type: pd.DataFrame,
    dim_status: pd.DataFrame,
    dim_engineer: pd.DataFrame,
    dim_equipment: pd.DataFrame,
    n_deliverables: int = N_DELIVERABLES,
) -> pd.DataFrame:
    """
    Creates the main fact table with one row per engineering deliverable.

    At this stage, the fact table is generated as a clean base.
    Data quality issues will be introduced later in data_quality.py.
    """

    project_ids = dim_project["project_id"].tolist()
    discipline_ids = dim_discipline["discipline_id"].tolist()
    document_type_ids = dim_document_type["document_type_id"].tolist()
    status_ids = dim_status["status_id"].tolist()
    equipment_ids = dim_equipment["equipment_id"].tolist()

    status_probabilities = [
        0.08,  # Not Started
        0.18,  # In Progress
        0.18,  # Under Review
        0.36,  # Approved
        0.08,  # Rejected
        0.10,  # Delayed
        0.02,  # Cancelled
    ]

    comments_options = [
        "",
        "Pending discipline review",
        "Waiting for client comments",
        "Metadata to be confirmed",
        "Requires engineering validation",
        "Manual update from legacy tracker",
    ]

    rows = []

    for i in range(1, n_deliverables + 1):
        project_id = random.choice(project_ids)
        discipline_id = random.choice(discipline_ids)
        document_type_id = random.choice(document_type_ids)
        equipment_id = random.choice(equipment_ids)

        responsible_engineer_id = get_engineer_for_discipline(
            discipline_id=discipline_id,
            dim_engineer=dim_engineer,
        )

        status_id = np.random.choice(
            status_ids,
            p=status_probabilities,
        )

        status_name = get_status_name(
            status_id=status_id,
            dim_status=dim_status,
        )

        planned_submission_date = DELIVERABLE_START_DATE + pd.to_timedelta(
            random.randint(0, DELIVERABLE_PLANNING_DAYS),
            unit="D",
        )

        planned_approval_date = planned_submission_date + pd.to_timedelta(
            random.randint(5, 25),
            unit="D",
        )

        actual_submission_date, actual_approval_date = generate_dates_for_status(
            status_name=status_name,
            planned_submission_date=planned_submission_date,
        )

        revision_number = np.random.choice(
            [0, 1, 2, 3, 4],
            p=[0.22, 0.35, 0.25, 0.13, 0.05],
        )

        review_cycle_count = max(
            0,
            revision_number + np.random.choice(
                [0, 1, 2],
                p=[0.65, 0.25, 0.10],
            ),
        )

        created_date = planned_submission_date - pd.to_timedelta(
            random.randint(20, 120),
            unit="D",
        )

        valid_dates = [
            date_value
            for date_value in [
                created_date,
                planned_submission_date,
                actual_submission_date,
                actual_approval_date,
            ]
            if pd.notna(date_value)
        ]

        last_updated_date = max(valid_dates) + pd.to_timedelta(
            random.randint(0, 10),
            unit="D",
        )

        document_type_name = get_document_type_name(
            document_type_id=document_type_id,
            dim_document_type=dim_document_type,
        )

        document_type_clean = clean_document_type_name(
            document_type_name=document_type_name,
        )

        document_id = (
            f"{project_id}-"
            f"{discipline_id[-3:]}-"
            f"{document_type_clean}-"
            f"{i:04d}"
        )

        document_title = (
            f"{document_type_name} for "
            f"{project_id} - "
            f"Package {random.randint(1, 20)}"
        )

        rows.append(
            {
                "deliverable_id": f"DEL-{i:05d}",
                "project_id": project_id,
                "document_id": document_id,
                "document_title": document_title,
                "discipline_id": discipline_id,
                "document_type_id": document_type_id,
                "equipment_id": equipment_id,
                "responsible_engineer_id": responsible_engineer_id,
                "status_id": status_id,
                "revision_number": revision_number,
                "planned_submission_date": planned_submission_date,
                "actual_submission_date": actual_submission_date,
                "planned_approval_date": planned_approval_date,
                "actual_approval_date": actual_approval_date,
                "review_cycle_count": review_cycle_count,
                "created_date": created_date,
                "last_updated_date": last_updated_date,
                "comments": random.choice(comments_options),
            }
        )

    return pd.DataFrame(rows)