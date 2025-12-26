'''
Utility functions for reading from and writing to Delta Lake tables
'''

import polars as pl
from deltalake import DeltaTable, write_deltalake
from pathlib import Path
from schemas import get_arrow_schema, apply_schema


'''
Read a Delta Lake table from the specified path into a Polars LazyFrame.

:param path: Path to the Delta Lake table.

:return: Polars LazyFrame containing the data from the Delta Lake table.
'''
def read_delta(path: Path) -> pl.LazyFrame:
    dt = DeltaTable(str(path))
    ds = dt.to_pyarrow_dataset()
    return pl.scan_pyarrow_dataset(ds)


'''
Write a Polars DataFrame to a Delta Lake table with the specified schema.

:param path: Path to the Delta Lake table.
:param df: Polars DataFrame to write.
:param schema_name: Name of the schema to apply.
:param mode: Write mode, either "overwrite" or "append" (default is "overwrite").
:param partition_by: List of columns to partition by (default is None).
'''
def write_with_schema(
    path: Path,
    df: pl.DataFrame,
    schema_name: str,
    mode: str = "overwrite",
    partition_by: list[str] | None = None,
):
    if df is None or df.height == 0:
        print(f"{path.name} - Empty DataFrame!")
        return

    path.mkdir(parents=True, exist_ok=True)

    # Aplies schema and converts to Arrow Table
    df_typed = apply_schema(df, schema_name)
    arrow_schema = get_arrow_schema(schema_name)
    arrow_table = df_typed.to_arrow()

    # Validates missing or extra columns
    expected_cols = set(arrow_schema.names)
    df_cols = set(df_typed.columns)
    missing = expected_cols - df_cols
    extra = df_cols - expected_cols

    if missing:
        print(f"{path.name} - Missing columns: {sorted(missing)}")
    if extra:
        print(f"{path.name} - Extra columns: {sorted(extra)}")

    # Writes to Delta Lake and applies schema
    write_deltalake(
        str(path),
        arrow_table,
        mode=mode,
        schema=arrow_schema,
        partition_by=partition_by,
        overwrite_schema=True,
    )

    print(f"{path.name}: {df_typed.height} rows written with schema '{schema_name}'!")

