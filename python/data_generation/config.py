from pathlib import Path
import pandas as pd


# ============================================================
# RANDOMNESS
# ============================================================

RANDOM_SEED = 42


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# ============================================================
# DATASET SIZE
# ============================================================

N_PROJECTS = 6
N_ENGINEERS = 45
N_EQUIPMENT = 120
N_DELIVERABLES = 750


# ============================================================
# DATE CONFIGURATION
# ============================================================

START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2026-12-31")

REFERENCE_DATE = pd.Timestamp("2026-07-04")


# ============================================================
# ENGINEERING DELIVERABLE DATE RANGE
# ============================================================

DELIVERABLE_START_DATE = pd.Timestamp("2025-03-01")
DELIVERABLE_PLANNING_DAYS = 580


# ============================================================
# DATA QUALITY ISSUE RATES
# ============================================================

MISSING_OWNER_RATE = 0.055
MISSING_EQUIPMENT_RATE = 0.075
MISSING_DISCIPLINE_RATE = 0.025
MISSING_DOCUMENT_TYPE_RATE = 0.025

DUPLICATE_DOCUMENT_ID_RATE = 0.04
INVALID_STATUS_RATE = 0.015
INVALID_DATE_RATE = 0.035
MISSING_APPROVAL_DATE_RATE = 0.07
INCONSISTENT_REVISION_RATE = 0.025
INVALID_EQUIPMENT_CRITICALITY_RATE = 0.03
MISSING_PROJECT_PHASE_RATE = 0.17


# ============================================================
# BUSINESS RULE PARAMETERS
# ============================================================

LONG_REVIEW_THRESHOLD_DAYS = 20

VALID_REVISION_MIN = 0
VALID_REVISION_MAX = 5