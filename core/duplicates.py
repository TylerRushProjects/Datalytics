from core.state import get_dataframe, set_dataframe, push_state
from utils.menus import show_duplicate_menu
import pandas as pd
from core.audit import log_action


def apply_duplicate_flow():
    """
    Full duplicate flow:
    1) Select one or more columns
    2) Choose identify or remove
    3) Apply duplicate logic

    Any invalid step -> return to main menu.
    """
    df = get_dataframe()

    if df is None:
        print("No file loaded. Please import a file first.")
        return

    # Step 1 – Pick column(s)
    print("\nAvailable Columns:")
    for idx, col in enumerate(df.columns, start=1):
        print(f"{idx}. {col}")

    print("\nYou may select MULTIPLE columns using comma-separated values.")
    print("Example: 1, 3   or   2,4,5")

    col_input = input("Enter column numbers: ").strip()

    if not col_input:
        print("No columns selected. Returning.")
        return

    # Parse comma-separated input like "1,3,4"
    try:
        indices = [int(x.strip()) for x in col_input.split(",")]
    except Exception:
        print("Invalid column input. Returning.")
        return

    # Range validation
    if any(idx < 1 or idx > len(df.columns) for idx in indices):
        print("One or more column selections are out of range.")
        return

    # Map indices → column names
    columns = [df.columns[i - 1] for i in indices]
    print(f"Columns selected for duplicate checking: ", ", ".join(columns))

    # Step 2 – Choose operation
    dup_choice = show_duplicate_menu()

    if dup_choice == "0":
        print("Duplicate operation cancelled.")
        return

    if dup_choice not in ("1", "2"):
        print("Invalid duplicate option. Returning.")
        return

    # Step 3 – Apply operation
    if dup_choice == "1":
        _identify_duplicates(df, columns)
    elif dup_choice == "2":
        push_state()  # allow Undo for destructive change
        _remove_duplicates(df, columns)


def _identify_duplicates(df: pd.DataFrame, columns: list):
    """
    Identify duplicates across selected columns.
    Shows duplicate rows but does NOT modify the DataFrame.
    Now offers optional export highlighting.
    """
    from core.state import set_duplicate_highlight

    duplicates = df[df.duplicated(subset=columns, keep=False)]

    if duplicates.empty:
        print("No duplicates found.")
        log_action(
            "DUP_IDENTIFY",
            details="No duplicates found.",
            conditions=f"subset={columns}",
            columns=columns,
            rows_affected=0,
        )
        return

    print("\n=== DUPLICATES FOUND ===")

    # Final output
    print(duplicates.head(20).to_string(index=False))
    print(f"\nTotal duplicate rows: {len(duplicates)}")

    # Log the duplicate identification action
    log_action(
        "DUP_IDENTIFY",
        details=f"Identified {len(duplicates)} duplicate rows.",
        conditions=f"subset={columns}",
        columns=columns,
        rows_affected=len(duplicates),
    )

    # Ask user if they'd like to highlight during export
    print("\nWould you like these duplicates highlighted in your next XLSX export?")
    print("1. Yes")
    print("2. No")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        info = {
            "columns": columns,
            "duplicate_index": duplicates.index.tolist()
        }
        set_duplicate_highlight(info)
        print("Highlighting enabled for export.")
    elif choice == "2":
        set_duplicate_highlight(None)
        print("Highlighting disabled.")
    else:
        print("Invalid choice. Returning.")


def _remove_duplicates(df: pd.DataFrame, columns: list):
    """
    Remove duplicates across selected columns.
    Keeps the first occurrence of each duplicate group.
    Updates the global DataFrame.
    """

    duplicates = df[df.duplicated(subset=columns, keep="first")]

    if duplicates.empty:
        print("No duplicates found.")
        log_action(
            "DUP_REMOVE",
            details="No duplicates found.",
            conditions=f"subset={columns}",
            columns=columns,
            rows_affected=0,
        )
        return  
    
    print("\n=== DUPLICATES TO BE REMOVED ===")
    print(duplicates.head(20).to_string(index=False))
    print(f"\nTotal duplicate rows: {len(duplicates)}")
    

    before = len(df)
    cleaned = df.drop_duplicates(subset=columns, keep="first")
    after = len(cleaned)

    # Final output
    print("\n=== DUPLICATE REMOVAL COMPLETE ===")
    print(f"Rows before: {before}")
    print(f"Rows after:  {after}")
    print(f"Duplicates removed: {before - after}")

    set_dataframe(cleaned)

    # Log the duplicate removal action
    log_action(
        "DUP_REMOVE",
        details=f"Removed {before - after} duplicate rows.",
        conditions=f"subset={columns}",
        columns=columns,
        rows_affected=before - after,
    )