import pandas as pd
from core.state import get_dataframe, set_dataframe, push_state
from utils.menus import show_format_menu
from core.audit import log_action


def apply_format_flow():
    """
    Full formatting flow:
    1) Select column
    2) Select formatting option
    3) Apply formatting & update DataFrame

    Any invalid step -> return to Transform Menu.
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
        print("Invalid column choice. Returning to menu.")
        return

    col_index = int(col_choice) - 1
    if col_index < 0 or col_index >= len(df.columns):
        print("Invalid column selection. Returning.")
        return

    column = df.columns[col_index]
    print(f"Column selected: {column}")

    # Step 2 — Select formatting operation
    format_map = {
        "1": "trim_whitespace",
        "2": "uppercase",
        "3": "lowercase",
        "4": "capitalize",
        "5": "short_date",
        "6": "long_date",
        "7": "decimal",
        "8": "percentage",
    }

    fmt_choice = show_format_menu()

    if fmt_choice == "0":
        print("Formatting cancelled.")
        return

    if fmt_choice not in format_map:
        print("Invalid formatting option. Returning.")
        return
    
    formatting = format_map[fmt_choice]
    print(f"Formatting option selected: {formatting}")

    # Step 3 — Apply formatting
    push_state()
    _apply_format(df, column, fmt_choice)


def _apply_format(df: pd.DataFrame, column: str, fmt_choice: str) -> None:
    """
    Internal formatting logic for the selected column and operation.
    Handles messy inputs and leaves unparseable values unchanged.
    """
    series = df[column]

    try:
        # 1. Trim whitespace
        if fmt_choice == "1":
            df[column] = series.astype(str).str.strip()

        # 2. Uppercase
        elif fmt_choice == "2":
            df[column] = series.astype(str).str.upper()

        # 3. Lowercase
        elif fmt_choice == "3":
            df[column] = series.astype(str).str.lower()

        # 4. Capitalize each word (Title Case)
        elif fmt_choice == "4":
            df[column] = series.astype(str).str.title()

        # 5. Short Date (MM/DD/YYYY)
        elif fmt_choice == "5":
            parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
            formatted = series.astype(str)  # start from original
            mask = parsed.notna()
            formatted[mask] = parsed[mask].dt.strftime("%m/%d/%Y")
            df[column] = formatted

        # 6. Long Date (Month DD, YYYY)
        elif fmt_choice == "6":
            parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
            formatted = series.astype(str)
            mask = parsed.notna()
            formatted[mask] = parsed[mask].dt.strftime("%B %d, %Y")
            df[column] = formatted

        # 7. Decimal (2 decimal places)
        elif fmt_choice == "7":
            numeric = pd.to_numeric(series, errors="coerce")
            formatted = series.astype(str)
            mask = numeric.notna()
            # format as 2 decimal places
            formatted[mask] = numeric[mask].round(2).map(lambda x: f"{x:.2f}")
            df[column] = formatted

        # 8. Percentage
        elif fmt_choice == "8":
            numeric = pd.to_numeric(series, errors="coerce")
            formatted = series.astype(str)
            mask = numeric.notna()

            # Values over 1 are assumed to be whole percentages
            def to_percent(v: float) -> str:
                if v <= 1:
                    v *= 100.0
                return f"{v:.0f}%"

            formatted[mask] = numeric[mask].map(to_percent)
            df[column] = formatted

        # Final output
        print("\n=== FORMAT RESULT ===")
        print(df.head(10).to_string(index=False))
        print("\nFormatting complete.")

        set_dataframe(df)

        # Log the formatting action
        log_action(
            "FORMAT",
            details=f"Applied formatting option '{fmt_choice}' on column '{column}'.",
            conditions=f"fmt_choice={fmt_choice}",
            columns=[column],
            # rows_affected is optional here; formatting generally affects whole column
        )

    # Catch any errors
    except Exception as e:
        print(f"Formatting error: {e}")