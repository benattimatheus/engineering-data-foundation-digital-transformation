import random

import numpy as np

from data_generation.config import (
    RANDOM_SEED,
    RAW_DATA_DIR,
)

from data_generation.dimensions import (
    create_dim_project,
    create_dim_discipline,
    create_dim_document_type,
    create_dim_status,
    create_dim_engineer,
    create_dim_equipment,
    create_dim_date,
)

from data_generation.fact_deliverables import create_fact_engineering_deliverables

from data_generation.data_quality import inject_data_quality_issues

from data_generation.export import (
    export_tables,
    print_table_summary,
)


# ============================================================
# SETUP
# ============================================================

def setup_environment() -> None:
    """
    Sets the random seed and creates the output folder.
    """

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Main execution flow for the synthetic data generation process.
    """

    setup_environment()

    # -----------------------------
    # Create dimensions
    # -----------------------------

    dim_discipline = create_dim_discipline()
    dim_document_type = create_dim_document_type()
    dim_status = create_dim_status()
    dim_project = create_dim_project()
    dim_engineer = create_dim_engineer(dim_discipline)
    dim_equipment = create_dim_equipment()
    dim_date = create_dim_date()

    # -----------------------------
    # Create fact table
    # -----------------------------

    fact_engineering_deliverables = create_fact_engineering_deliverables(
        dim_project=dim_project,
        dim_discipline=dim_discipline,
        dim_document_type=dim_document_type,
        dim_status=dim_status,
        dim_engineer=dim_engineer,
        dim_equipment=dim_equipment,
    )

    # -----------------------------
    # Inject data quality issues
    # -----------------------------

    inject_data_quality_issues(
        fact_engineering_deliverables=fact_engineering_deliverables,
        dim_equipment=dim_equipment,
        dim_project=dim_project,
    )

    # -----------------------------
    # Export tables
    # -----------------------------

    tables = {
        "fact_engineering_deliverables.csv": fact_engineering_deliverables,
        "dim_project.csv": dim_project,
        "dim_discipline.csv": dim_discipline,
        "dim_document_type.csv": dim_document_type,
        "dim_status.csv": dim_status,
        "dim_engineer.csv": dim_engineer,
        "dim_equipment.csv": dim_equipment,
        "dim_date.csv": dim_date,
    }

    export_tables(tables)

    print_table_summary(tables)

    print("\nDataset generated successfully.")
    print(f"Output folder: {RAW_DATA_DIR.resolve()}")


if __name__ == "__main__":
    main()