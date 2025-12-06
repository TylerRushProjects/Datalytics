import pandas as pd
from core.state import get_dataframe, set_dataframe, push_state
from utils.menus import show_condition_menu
from core.audit import log_action


def apply_filter_flow():
    """
    Full filtering flow:
    1) Select column
    2) Select condition
    3) Enter value
    4) Apply filter & update DataFrame

    Any invalid step -> cancel and return to the Transform Menu.
    """
    df = get_dataframe()

    if df is None:
        print("No file loaded. Please import a file first.")
        return

    # Step 1 — Column selection
    print("\nAvailable Columns:")
    for idx, col in enumerate(df.columns, start=1):
        print(f"{idx}. {col}")

    col_choice = input("Select column number: ").strip()

    if not col_choice.isdigit():
        print("Invalid column choice. Returning.")
        return

    col_index = int(col_choice)
    if col_index < 1 or col_index > len(df.columns):
        print("Invalid column selection. Returning.")
        return

    column = df.columns[col_index - 1]
    print(f"Column selected: {column}")

    # Step 2 — Condition selection
    condition_map = {
        "1": "equals",
        "2": "not_equals",
        "3": "contains",
        "4": "not_contains",
        "5": "greater_than",
        "6": "less_than",
    }

    cond_choice = show_condition_menu()

    if cond_choice == "0":
        print("Filter cancelled.")
        return

    if cond_choice not in condition_map:
        print("Invalid condition. Returning.")
        return

    condition = condition_map[cond_choice]
    print(f"Condition selected: {condition}")

    # Step 3 — Value input
    value = input("Enter filter value: ").strip()
    if value == "":
        print("Empty values are not allowed.")
        return

    # Step 4 — Apply filter
    push_state()  # Save state for Undo
    _apply_filter(df, column, condition, value)


def _apply_filter(df, column, condition, value):
    """Internal filtering implementation."""
    series = df[column]

    try:
        if condition in ("greater_than", "less_than"):
            series_numeric = pd.to_numeric(series, errors="coerce")
            value_num = float(value)

            if condition == "greater_than":
                filtered = df[series_numeric > value_num]
            else:
                filtered = df[series_numeric < value_num]

        elif condition in ("equals", "not_equals"):
            if series.dtype.kind in {"i", "f"}:
                value_num = float(value)
                mask = (series == value_num)
            else:
                s = series.astype(str)
                mask = (s == value)

            filtered = df[mask] if condition == "equals" else df[~mask]

        elif condition in ("contains", "not_contains"):
            s = series.astype(str).str.lower()
            v = value.lower()
            mask = s.str.contains(v, na=False)
            filtered = df[mask] if condition == "contains" else df[~mask]

        else:
            print("Invalid condition.")
            return

        # Show results
        print("\n=== FILTER RESULT ===")
        print(filtered.head(10).to_string(index=False))
        print(f"Rows after filtering: {len(filtered)}")

        # Update global DataFrame
        set_dataframe(filtered)

        log_action(
            "FILTER",
            details=f"Filtered on column '{column}' with condition '{condition}' and value '{value}'.",
            conditions=f"{column} {condition} {value}",
            columns=[column],
            rows_affected=len(filtered),
        )

    except ValueError:
        print("Invalid numeric input for this condition.")