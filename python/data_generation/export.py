from pathlib import Path

import pandas as pd

from data_generation.config import RAW_DATA_DIR


# ============================================================
# EXPORT FUNCTIONS
# ============================================================

def export_table(
    dataframe: pd.DataFrame,
    file_name: str,
    output_dir: Path = RAW_DATA_DIR,
) -> Path:
    """
    Exports a single DataFrame as a CSV file.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / file_name

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )

    return output_path


def export_tables(
    tables: dict[str, pd.DataFrame],
    output_dir: Path = RAW_DATA_DIR,
) -> None:
    """
    Exports multiple DataFrames as CSV files.
    """

    for file_name, dataframe in tables.items():
        export_table(
            dataframe=dataframe,
            file_name=file_name,
            output_dir=output_dir,
        )


# ============================================================
# SUMMARY FUNCTIONS
# ============================================================

def print_table_summary(
    tables: dict[str, pd.DataFrame],
) -> None:
    """
    Prints a summary of generated tables.
    """

    print("\nGenerated tables:")
    print("-" * 70)

    for table_name, dataframe in tables.items():
        print(
            f"{table_name}: "
            f"{len(dataframe):,} rows | "
            f"{len(dataframe.columns)} columns"
        )

    print("-" * 70)