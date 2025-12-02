

def require_menu_choice(prompt: str, valid_options: set[str]) -> str:
    """
    Prompt for menu input and ensure the returned value
    is one of the allowed options.
    """
    while True:
        value = input(prompt).strip()

        if value in valid_options:
            return value

        print("Invalid option. Please try again.")