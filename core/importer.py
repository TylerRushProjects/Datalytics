import pandas as pd
from pathlib import Path
from core.state import set_dataframe, reset_state
from core.audit import log_action, clear_audit_log

def validate_headers_raw(path: str) -> None:
    """
    Validate headers BEFORE pandas auto-renames duplicates.
    Detect blank or duplicate header names from the raw file.
    """
    ext = Path(path).suffix.lower()

    # Read first header row manually
    if ext == ".csv":
        with open(path, "r", encoding="utf-8") as f:
            raw_header = f.readline().strip().split(",")
    else:
        # XLSX: read header row using pandas without renaming
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        sheet = wb.active
        raw_header = [cell.value for cell in next(sheet.iter_rows(max_row=1))]

    # Check for blank headers
    if any(h is None or str(h).strip() == "" for h in raw_header):
        raise ValueError("Invalid header: one or more column names are blank.")

    # Check for duplicates in raw header row
    if len(raw_header) != len(set(raw_header)):
        raise ValueError("Invalid header: duplicate column names detected.")

def validate_path_exists(path: str) -> None:
    """
    Ensure the provided file path exists on disk.
    Raises FileNotFoundError if the file does not exist.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")

def load_file(path: str) -> pd.DataFrame:
    validate_path_exists(path)

    ext = Path(path).suffix.lower()

    # IMP-4: Validate raw headers first
    validate_headers_raw(path)

    # Now safely load with pandas
    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file type: '{ext}'. Only .csv and .xlsx are allowed.")

    # BEFORE we start using this new DataFrame, reset state and audit
    reset_state()
    clear_audit_log()

    # now set the new active DataFrame
    set_dataframe(df, path)

    # log this new import as the first action in this "session" of the dataset
    log_action(
        "IMPORT",
        details=f"Imported file '{path}'",
        rows_affected=len(df)
    )

    return df

def get_file_summary(df: pd.DataFrame) -> dict:
    """
    Return basic metadata for a loaded DataFrame.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "headers": list(df.columns)
    }