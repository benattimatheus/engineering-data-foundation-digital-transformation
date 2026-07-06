import random

import numpy as np
import pandas as pd

from data_generation.config import (
    N_DELIVERABLES,
    REFERENCE_DATE,
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

def get_project_dates(
    project_id: str,
    dim_project: pd.DataFrame,
) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Returns project start and end dates.
    """

    project_row = dim_project.loc[
        dim_project["project_id"] == project_id
    ].iloc[0]

    return (
        pd.Timestamp(project_row["project_start_date"]),
        pd.Timestamp(project_row["project_end_date"]),
    )

def generate_dates_for_status(
    status_name: str,
    planned_submission_date: pd.Timestamp,
    planned_approval_date: pd.Timestamp,
    project_start_date: pd.Timestamp,
    reference_date: pd.Timestamp = REFERENCE_DATE,
) -> tuple[pd.Timestamp | pd.NaT, pd.Timestamp | pd.NaT]:
    """
    Generates actual dates according to deliverable status.
    Actual dates cannot be after the reference date.
    """

    max_actual_date = min(reference_date, planned_approval_date)

    if status_name == "Not Started":
        return pd.NaT, pd.NaT

    if status_name == "In Progress":
        return pd.NaT, pd.NaT

    if status_name == "Delayed":
        return pd.NaT, pd.NaT

    if status_name == "Cancelled":
        return pd.NaT, pd.NaT

    if status_name == "Under Review":
        latest_submission_date = min(reference_date, planned_approval_date)

        actual_submission_date = planned_submission_date + pd.to_timedelta(
            random.randint(-5, 10),
            unit="D",
        )

        if actual_submission_date < project_start_date:
            actual_submission_date = project_start_date

        if actual_submission_date > latest_submission_date:
            actual_submission_date = latest_submission_date

        return actual_submission_date, pd.NaT

    if status_name == "Rejected":
        latest_submission_date = min(reference_date, planned_approval_date)

        actual_submission_date = planned_submission_date + pd.to_timedelta(
            random.randint(-5, 15),
            unit="D",
        )

        if actual_submission_date < project_start_date:
            actual_submission_date = project_start_date

        if actual_submission_date > latest_submission_date:
            actual_submission_date = latest_submission_date

        return actual_submission_date, pd.NaT

    if status_name == "Approved":
        latest_approval_date = min(reference_date, planned_approval_date + pd.to_timedelta(15, unit="D"))

        actual_submission_date = planned_submission_date + pd.to_timedelta(
            random.randint(-5, 10),
            unit="D",
        )

        if actual_submission_date < project_start_date:
            actual_submission_date = project_start_date

        if actual_submission_date > latest_approval_date:
            actual_submission_date = latest_approval_date - pd.to_timedelta(2, unit="D")

        actual_approval_date = actual_submission_date + pd.to_timedelta(
            random.randint(2, 15),
            unit="D",
        )

        if actual_approval_date > reference_date:
            actual_approval_date = reference_date

        if actual_approval_date < actual_submission_date:
            actual_approval_date = actual_submission_date

        return actual_submission_date, actual_approval_date

    return pd.NaT, pd.NaT


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

        project_start_date, project_end_date = get_project_dates(
            project_id=project_id,
            dim_project=dim_project,
        )

        latest_planned_submission_date = project_end_date - pd.to_timedelta(
            25,
            unit="D",
        )

        if latest_planned_submission_date < project_start_date:
            latest_planned_submission_date = project_start_date

        available_days = max(
            1,
            (latest_planned_submission_date - project_start_date).days,
        )

        planned_submission_date = project_start_date + pd.to_timedelta(
            random.randint(0, available_days),
            unit="D",
        )

        planned_approval_date = planned_submission_date + pd.to_timedelta(
            random.randint(5, 25),
            unit="D",
        )

        if planned_approval_date > project_end_date:
            planned_approval_date = project_end_date

        if planned_submission_date > REFERENCE_DATE:
            status_id = np.random.choice(
                ["STAT-001", "STAT-002"],
                p=[0.70, 0.30],
            )
        else:
            status_id = np.random.choice(
                status_ids,
                p=status_probabilities,
            )

        status_name = get_status_name(
            status_id=status_id,
            dim_status=dim_status,
        )

        actual_submission_date, actual_approval_date = generate_dates_for_status(
            status_name=status_name,
            planned_submission_date=planned_submission_date,
            planned_approval_date=planned_approval_date,
            project_start_date=project_start_date,
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

        if created_date > REFERENCE_DATE:
            created_date = REFERENCE_DATE - pd.to_timedelta(
                random.randint(30, 120),
                unit="D",
            )

        if created_date < project_start_date:
            created_date = project_start_date

        if created_date > REFERENCE_DATE:
            created_date = REFERENCE_DATE

        valid_dates = [
            date_value
            for date_value in [
                created_date,
                actual_submission_date,
                actual_approval_date,
            ]
            if pd.notna(date_value) and date_value <= REFERENCE_DATE
        ]

        if valid_dates:
            last_updated_date = max(valid_dates) + pd.to_timedelta(
                random.randint(0, 10),
                unit="D",
            )
        else:
            last_updated_date = created_date

        if last_updated_date > REFERENCE_DATE:
            last_updated_date = REFERENCE_DATE

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