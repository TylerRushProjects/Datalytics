current_df = None
current_file_path = None
history_stack = []

data_version = 0  # increments whenever the DataFrame changes

duplicate_highlight_info = None  # stores info for export highlighting

def reset_state():
    """
    Reset all shared state when a new file is imported.
    This clears the current DataFrame, history, version, and highlight info.
    """
    global current_df, current_file_path, history_stack, data_version, duplicate_highlight_info
    current_df = None
    current_file_path = None
    history_stack = []
    data_version = 0
    duplicate_highlight_info = None


def set_dataframe(df, path=None):
    """
    Set the active DataFrame and optionally update the file path.
    Increments data_version because the data has changed.
    """
    global current_df, current_file_path, data_version
    current_df = df
    if path:
        current_file_path = path
    data_version += 1


def get_dataframe():
    return current_df


def get_data_version():
    """Return the current version number of the active DataFrame."""
    return data_version


def push_state():
    """
    Save a copy of the current DataFrame and its version for Undo.
    """
    if current_df is not None:
        history_stack.append((current_df.copy(), data_version))


def undo_last():
    """
    Restore the most recent DataFrame and its version.
    Does NOT automatically clear highlight info, but will
    cause it to be treated as stale if versions don't match.
    """
    global current_df, data_version
    if not history_stack:
        print("No previous action to undo.")
        return False
    prev_df, prev_version = history_stack.pop()
    current_df = prev_df
    data_version = prev_version
    print("Last action undone.")
    return True


def set_duplicate_highlight(info):
    """
    Store or clear duplicate highlight configuration.
    When storing, we attach the current data_version so we
    can later detect whether the data has changed since Identify.
    """
    global duplicate_highlight_info

    if info is None:
        duplicate_highlight_info = None
    else:
        # attach the data_version at the moment Identify ran
        info["data_version"] = data_version
        duplicate_highlight_info = info


def get_duplicate_highlight():
    """Return the current duplicate highlight configuration, if any."""
    return duplicate_highlight_info