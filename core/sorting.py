import pandas as pd
from core.state import get_dataframe, set_dataframe, push_state
from utils.menus import show_sort_direction_menu
from core.audit import log_action

def apply_sort_flow():
    """
    Full sorting flow:
    1) Select column
    2) Select ascending/descending
    3) Apply sort and update state

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
        print("Invalid choice. Returning.")
        return

    col_index = int(col_choice)
    if col_index < 1 or col_index > len(df.columns):
        print("Invalid column selection. Returning.")
        return

    column = df.columns[col_index - 1]
    print(f"Column selected: {column}")

    # Step 2 — Sort direction
    direction_choice = show_sort_direction_menu()

    if direction_choice == "0":
        print("Sort cancelled.")
        return

    if direction_choice not in ("1", "2"):
        print("Invalid direction. Returning.")
        return

    ascending = (direction_choice == "1")
    print(f"Sorting in {'ascending' if ascending else 'descending'} order.")

    # Step 3 — Apply sort
    push_state()  # allow Undo
    _apply_sort(df, column, ascending)


def _apply_sort(df, column, ascending):
    """Internal helper to sort the DataFrame."""
    try:
        sorted_df = df.sort_values(by=column, ascending=ascending)

        print("\n=== SORT RESULT ===")
        print(sorted_df.head(10).to_string(index=False))
        print(f"\nRows total: {len(sorted_df)}")

        set_dataframe(sorted_df)

        log_action(
            "SORT",
            details=f"Sorted by column '{column}' in {'ascending' if ascending else 'descending'} order.",
            conditions=f"{column} {'ASC' if ascending else 'DESC'}",
            columns=[column],
            rows_affected=len(sorted_df),
        )

    except Exception as e:
        print(f"Error during sorting: {e}")