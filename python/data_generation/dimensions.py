import random

import numpy as np
import pandas as pd

from data_generation.config import (
    N_PROJECTS,
    N_ENGINEERS,
    N_EQUIPMENT,
    START_DATE,
    END_DATE,
)


# ============================================================
# DIMENSION: DISCIPLINE
# ============================================================

def create_dim_discipline() -> pd.DataFrame:
    """
    Creates the engineering discipline dimension.

    Each discipline represents an engineering area responsible
    for creating or reviewing project deliverables.
    """

    data = [
        ("DISC-001", "Process"),
        ("DISC-002", "Mechanical"),
        ("DISC-003", "Electrical"),
        ("DISC-004", "Automation"),
        ("DISC-005", "Civil"),
        ("DISC-006", "Project Management"),
    ]

    columns = [
        "discipline_id",
        "discipline_name",
    ]

    return pd.DataFrame(data, columns=columns)


# ============================================================
# DIMENSION: DOCUMENT TYPE
# ============================================================

def create_dim_document_type() -> pd.DataFrame:
    """
    Creates the document type dimension.

    Each document type represents a common engineering deliverable
    produced during project execution.
    """

    data = [
        ("DOC-001", "P&ID"),
        ("DOC-002", "Equipment List"),
        ("DOC-003", "Datasheet"),
        ("DOC-004", "Layout Drawing"),
        ("DOC-005", "Specification"),
        ("DOC-006", "Validation Document"),
        ("DOC-007", "Engineering Report"),
    ]

    columns = [
        "document_type_id",
        "document_type_name",
    ]

    return pd.DataFrame(data, columns=columns)


# ============================================================
# DIMENSION: STATUS
# ============================================================

def create_dim_status() -> pd.DataFrame:
    """
    Creates the status dimension.

    The status group helps simplify reporting in Power BI,
    allowing detailed status and grouped workflow analysis.
    """

    data = [
        ("STAT-001", "Not Started", "Open"),
        ("STAT-002", "In Progress", "Open"),
        ("STAT-003", "Under Review", "Review"),
        ("STAT-004", "Approved", "Closed"),
        ("STAT-005", "Rejected", "Review"),
        ("STAT-006", "Delayed", "Open"),
        ("STAT-007", "Cancelled", "Closed"),
    ]

    columns = [
        "status_id",
        "status_name",
        "status_group",
    ]

    return pd.DataFrame(data, columns=columns)


# ============================================================
# DIMENSION: PROJECT
# ============================================================

def create_dim_project(n_projects: int = N_PROJECTS) -> pd.DataFrame:
    """
    Creates the project dimension.

    Each row represents an engineering project managed by the company.
    """

    project_names = [
        f"Engineering Project {i:02d}"
        for i in range(1, n_projects + 1)
    ]

    clients = [
        "NovoPharma",
        "BioNordic",
        "MedCore",
        "PharmaPlus",
        "LifeSciences Group",
    ]

    project_phases = [
        "Concept",
        "Basic Design",
        "Detailed Design",
        "Construction",
        "Commissioning",
        "Qualification",
    ]

    project_statuses = [
        "Active",
        "On Hold",
        "Completed",
        "Delayed",
    ]

    project_start_dates = pd.Series(
        pd.date_range(
            start="2025-01-01",
            end="2025-10-01",
            periods=n_projects,
        )
    )

    project_duration_days = np.random.randint(
        240,
        520,
        size=n_projects,
    )

    project_end_dates = project_start_dates + pd.to_timedelta(
        project_duration_days,
        unit="D",
    )

    dim_project = pd.DataFrame(
        {
            "project_id": [
                f"PRJ-{i:03d}"
                for i in range(1, n_projects + 1)
            ],
            "project_name": project_names[:n_projects],
            "client": np.random.choice(
                clients,
                size=n_projects,
            ),
            "project_phase": np.random.choice(
                project_phases,
                size=n_projects,
                p=[0.05, 0.15, 0.35, 0.25, 0.10, 0.10],
            ),
            "project_manager": [
                f"Project Manager {i}"
                for i in range(1, n_projects + 1)
            ],
            "project_start_date": project_start_dates,
            "project_end_date": project_end_dates,
            "project_status": np.random.choice(
                project_statuses,
                size=n_projects,
                p=[0.60, 0.10, 0.15, 0.15],
            ),
        }
    )

    return dim_project


# ============================================================
# DIMENSION: ENGINEER
# ============================================================

def create_dim_engineer(
    dim_discipline: pd.DataFrame,
    n_engineers: int = N_ENGINEERS,
) -> pd.DataFrame:
    """
    Creates the engineer dimension.

    Each engineer is assigned to one main discipline.
    This allows analysis by owner, team, location, role, and discipline.
    """

    first_names = [
        "Emma", "Lucas", "Sofia", "Noah", "Olivia",
        "Liam", "Ava", "Mia", "Ethan", "Isabella",
        "Leo", "Amelia", "Oscar", "Ella", "Hugo",
        "Freja", "Maja", "William", "Clara", "Felix",
    ]

    last_names = [
        "Andersen", "Nielsen", "Hansen", "Jensen", "Larsen",
        "Moller", "Pedersen", "Schmidt", "Rasmussen",
        "Johansson", "Berg", "Silva", "Santos", "Costa",
        "Oliveira",
    ]

    roles = [
        "Junior Engineer",
        "Engineer",
        "Senior Engineer",
        "Lead Engineer",
        "Discipline Lead",
    ]

    teams = [
        "Team Alpha",
        "Team Beta",
        "Team Gamma",
        "Team Delta",
    ]

    locations = [
        "Denmark",
        "India",
        "United States",
        "Brazil",
        "Poland",
    ]

    discipline_ids = dim_discipline["discipline_id"].tolist()

    rows = []

    for i in range(1, n_engineers + 1):
        discipline_id = random.choice(discipline_ids)

        rows.append(
            {
                "responsible_engineer_id": f"ENG-{i:03d}",
                "engineer_name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "role": random.choice(roles),
                "discipline_id": discipline_id,
                "team": random.choice(teams),
                "location": random.choice(locations),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# DIMENSION: EQUIPMENT
# ============================================================

def create_dim_equipment(n_equipment: int = N_EQUIPMENT) -> pd.DataFrame:
    """
    Creates the equipment dimension.

    Equipment is useful for connecting engineering deliverables
    to systems, areas, equipment types, and criticality.
    """

    equipment_types = [
        "Pump",
        "Tank",
        "Heat Exchanger",
        "Valve",
        "Control Panel",
        "Pipe System",
        "Reactor",
        "Filter",
    ]

    equipment_prefix = {
        "Pump": "P",
        "Tank": "T",
        "Heat Exchanger": "HX",
        "Valve": "V",
        "Control Panel": "CP",
        "Pipe System": "PS",
        "Reactor": "R",
        "Filter": "F",
    }

    areas = [
        "Area 100",
        "Area 200",
        "Area 300",
        "Area 400",
        "Utility Area",
        "Cleanroom Area",
    ]

    systems = [
        "Process System",
        "CIP System",
        "WFI System",
        "HVAC System",
        "Automation System",
        "Electrical System",
    ]

    criticalities = [
        "High",
        "Medium",
        "Low",
    ]

    rows = []

    for i in range(1, n_equipment + 1):
        equipment_type = random.choice(equipment_types)
        prefix = equipment_prefix[equipment_type]

        rows.append(
            {
                "equipment_id": f"EQ-{i:04d}",
                "equipment_tag": f"{prefix}-{1000 + i}",
                "equipment_type": equipment_type,
                "area": random.choice(areas),
                "system": random.choice(systems),
                "criticality": random.choice(criticalities),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# DIMENSION: DATE
# ============================================================

def create_dim_date(
    start_date: pd.Timestamp = START_DATE,
    end_date: pd.Timestamp = END_DATE,
) -> pd.DataFrame:
    """
    Creates a standard date dimension.

    This table will be used in Power BI for time-based analysis,
    such as trends, overdue deliverables, submissions, and approvals.
    """

    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D",
    )

    dim_date = pd.DataFrame(
        {
            "date": date_range,
            "year": date_range.year,
            "quarter": [f"Q{quarter}" for quarter in date_range.quarter],
            "month": date_range.month,
            "month_name": date_range.strftime("%B"),
            "week": date_range.isocalendar().week.astype(int),
            "day": date_range.day,
            "weekday": date_range.strftime("%A"),
            "is_weekend": date_range.weekday >= 5,
        }
    )

    return dim_date