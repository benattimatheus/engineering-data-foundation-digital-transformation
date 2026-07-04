"""
Engineering Data Foundation & Digital Transformation Dashboard
Synthetic Dataset Generator

This script generates CSV tables for an engineering data analytics portfolio project.

Generated tables:
- fact_engineering_deliverables.csv
- dim_project.csv
- dim_discipline.csv
- dim_document_type.csv
- dim_status.csv
- dim_engineer.csv
- dim_equipment.csv
- dim_date.csv

Main objective:
Simulate an engineering company moving from document-based project tracking
to structured, data-driven reporting with data quality rules.
"""

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
# EXPORT
# ============================================================

def export_table(dataframe, file_name: str) -> None:
    """
    Exports a dataframe as a CSV file.
    """

    output_path = RAW_DATA_DIR / file_name

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )


# ============================================================
# SUMMARY
# ============================================================

def print_table_summary(tables: dict) -> None:
    """
    Prints a simple summary of generated tables.
    """

    print("\nGenerated tables:")
    print("-" * 60)

    for table_name, dataframe in tables.items():
        print(
            f"{table_name}: "
            f"{len(dataframe):,} rows | "
            f"{len(dataframe.columns)} columns"
        )

    print("-" * 60)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Main execution flow for the synthetic data generation process.
    """

    setup_environment()

    dim_discipline = create_dim_discipline()
    dim_document_type = create_dim_document_type()
    dim_status = create_dim_status()
    dim_project = create_dim_project()
    dim_engineer = create_dim_engineer(dim_discipline)
    dim_equipment = create_dim_equipment()
    dim_date = create_dim_date()

    tables = {
        "dim_project.csv": dim_project,
        "dim_discipline.csv": dim_discipline,
        "dim_document_type.csv": dim_document_type,
        "dim_status.csv": dim_status,
        "dim_engineer.csv": dim_engineer,
        "dim_equipment.csv": dim_equipment,
        "dim_date.csv": dim_date,
    }

    for file_name, dataframe in tables.items():
        export_table(
            dataframe=dataframe,
            file_name=file_name,
        )

    print_table_summary(tables)

    print("\nDimension tables generated successfully.")
    print(f"Output folder: {RAW_DATA_DIR.resolve()}")


if __name__ == "__main__":
    main()