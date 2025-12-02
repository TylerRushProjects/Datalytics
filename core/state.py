current_df = None
current_file_path = None

# stack to store DataFrames for undo
history_stack = []

def set_dataframe(df, path=None):
    """Store the active DataFrame and optional file path."""
    global current_df, current_file_path
    current_df = df
    if path:
        current_file_path = path

def get_dataframe():
    """Return the active DataFrame."""
    return current_df

def push_state():
    """
    Save a copy of the current DataFrame to the undo stack.
    Called BEFORE any transformation such as filtering, sorting, etc.
    """
    if current_df is not None:
        history_stack.append(current_df.copy())


def undo_last():
    """
    Restore the most recent DataFrame from the undo stack.
    Returns True if restored, False if no history exists.
    """
    global current_df
    if not history_stack:
        return False
    current_df = history_stack.pop()
    return True