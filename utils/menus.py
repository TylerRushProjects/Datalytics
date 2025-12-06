def show_main_menu():
    """Display the main menu options."""
    print("\n=== DATALYTICS ===")
    print("1. Import File")
    print("2. Transform Data")
    print("3. Duplicate Detection")
    print("4. Audit Log")
    print("5. Export Data")
    print("6. Undo Last Action")
    print("0. Exit")

def show_transform_menu():
    """Display the Transform submenu options."""
    print("\n=== TRANSFORM MENU ===")
    print("1. Filter")
    print("2. Sort")
    print("3. Format")
    print("0. Back")
    return input("Enter choice: ").strip()

def show_condition_menu():
    """Display available filter conditions."""
    print("\n=== FILTER CONDITIONS ===")
    print("1. Equals")
    print("2. Not Equals")
    print("3. Contains")
    print("4. Does Not Contain")
    print("5. Greater Than")
    print("6. Less Than")
    print("0. Back")
    return input("Enter choice: ").strip()

def show_sort_direction_menu():
    """Display sorting direction options."""
    print("\n=== SORT DIRECTION ===")
    print("1. Ascending")
    print("2. Descending")
    print("0. Cancel")
    return input("Enter choice: ").strip()

def show_format_menu():
    """Display formatting operations."""
    print("\n=== FORMAT OPTIONS ===")
    print("1. Trim Whitespace")
    print("2. Uppercase Text")
    print("3. Lowercase Text")
    print("4. Capitalize Each Word")
    print("5. Convert to Short Date (MM/DD/YYYY)")
    print("6. Convert to Long Date (Month DD, YYYY)")
    print("7. Convert to Decimal (2 decimal places)")
    print("8. Convert to Percentage")
    print("0. Cancel")
    return input("Enter choice: ").strip()

def show_duplicate_menu():
    """Display duplicate handling options."""
    print("\n=== DUPLICATE OPTIONS ===")
    print("1. Identify Duplicates Only")
    print("2. Remove Duplicates")
    print("0. Cancel")
    return input("Enter choice: ").strip()

def show_export_menu():
    """Display export options."""
    print("\n=== EXPORT MENU ===")
    print("1. Export as CSV")
    print("2. Export as XLSX")
    print("0. Back")
    return input("Enter choice: ").strip()