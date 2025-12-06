

import sys
from utils.menus import show_main_menu
from utils.validation import require_menu_choice
import core.audit

def main():
    """Main application loop that accepts and routes user actions."""
    valid = {"0", "1", "2", "3", "4", "5", "6"}

    while True:
        show_main_menu()
        choice = require_menu_choice("Enter choice: ", valid)

        if choice == "1":
            print("Import selected (IMP).")
            path = input("Enter file path (.csv or .xlsx): ").strip()

            try:
                from core.importer import load_file, get_file_summary
                from core.state import set_dataframe

                df = load_file(path)
                summary = get_file_summary(df)

                print("\n=== FILE LOADED SUCCESSFULLY ===")
                print(f"Rows: {summary['rows']}")
                print(f"Columns: {summary['columns']}")
                print("Headers:", summary["headers"])
                print("\nPreview (first 5 rows):")
                print(df.head().to_string(index=False))

                set_dataframe(df, path)

            except Exception as e:
                print("\nERROR: File could not be loaded.")
                print(str(e))
        elif choice == "2":
            from utils.menus import show_transform_menu
            from core.filtering import apply_filter_flow

            while True:
                t_choice = show_transform_menu()

                if t_choice == "1":  # Apply Filter
                    apply_filter_flow()

                elif t_choice == "2":
                    from core.sorting import apply_sort_flow
                    apply_sort_flow()

                elif t_choice == "3":
                    from core.formatting import apply_format_flow
                    apply_format_flow()

                elif t_choice == "0":
                    break

                else:
                    print("Invalid choice.")
        elif choice == "3":
            from core.duplicates import apply_duplicate_flow
            apply_duplicate_flow()
        elif choice == "4":
            from core.audit import print_audit_log
            print_audit_log()
        elif choice == "5":
            from core.exporter import export_flow
            export_flow()
        elif choice == "6":
            from core.state import undo_last
            from core.audit import log_action
            if undo_last():
                print("Last action undone.")
                log_action(
                    "UNDO",
                    details="Reverted the most recent data transformation."
                )
            else:
                print("No previous action to undo.")
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()