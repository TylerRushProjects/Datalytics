

import sys
from core.audit import log_action
from utils.menus import show_main_menu
from utils.validation import require_menu_choice

def main():
    """Main application loop that accepts and routes user actions."""
    valid = {"0", "1", "2", "3", "4", "5", "6"}

    while True:
        show_main_menu()
        choice = require_menu_choice("Enter choice: ", valid)

        # Import Action
        if choice == "1":
            from core.importer import load_file
            load_file()


        # Transform Actions
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


        # Duplicate Action
        elif choice == "3":
            from core.duplicates import apply_duplicate_flow
            apply_duplicate_flow()
            

        # Audit Action
        elif choice == "4":
            from core.audit import print_audit_log
            print_audit_log()


        # Export Action
        elif choice == "5":
            from core.exporter import export_flow
            export_flow()


        # Undo Action
        elif choice == "6":
            from core.state import undo_last
            
            if undo_last():
                log_action(
                    "UNDO",
                    details="Reverted the most recent data transformation."
                )


        # Exit Action
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()