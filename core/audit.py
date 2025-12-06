import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "datalytics_audit.db"))


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def _init_db():
    """Create the audit_log table if it does not exist, and clear it for this run."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                action_type TEXT NOT NULL,
                conditions TEXT,
                columns TEXT,
                rows_affected INTEGER,
                details TEXT
            );
            """
        )
        conn.commit()
    finally:
        conn.close()

    # After ensuring the table exists, clear any old rows from previous runs
    clear_audit_log()


def clear_audit_log():
    """Delete all rows from the audit_log table."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM audit_log;")
        conn.commit()
    finally:
        conn.close()


# Initialize DB and clear any previous data when module is first imported
_init_db()


def log_action(action_type, details="", conditions=None, columns=None, rows_affected=None):
    """Insert one action into the audit_log table."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colstr = ",".join(columns) if columns else None

    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_log (time, action_type, conditions, columns, rows_affected, details)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (timestamp, action_type, conditions, colstr, rows_affected, details),
        )
        conn.commit()
    finally:
        conn.close()


def get_audit_log():
    """Return list of log entries."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM audit_log ORDER BY id")
        rows = cur.fetchall()
    finally:
        conn.close()

    return rows


def print_audit_log():
    """Pretty-print audit entries to the terminal."""
    rows = get_audit_log()

    print("\n=== AUDIT LOG ===")
    if not rows:
        print("No audit entries found.")
        return

    for row in rows:
        id, time, action_type, conditions, columns, rows_affected, details = row
        print(f"{id}. [{time}] {action_type}")
        print(f"   Conditions:    {conditions if conditions else '-'}")
        print(f"   Columns:       {columns if columns else '-'}")
        print(f"   Rows affected: {rows_affected if rows_affected is not None else '-'}")
        print(f"   Details:       {details if details else '-'}\n")

def save_audit_log_to_txt(path: str):
    """
    Save the audit log to a text file located in the same folder as 'path'.
    The file name is derived from the export file name.
    """
    directory = os.path.dirname(os.path.abspath(path))
    base = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join(directory, f"{base}_audit_log.txt")

    entries = get_audit_log()

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("=== DATALYTICS AUDIT LOG ===\n\n")

            for entry in entries:
                id, time, action_type, conditions, columns, rows_affected, details = entry
                f.write(f"{id}. [{time}] {action_type}\n")
                f.write(f"   Conditions:    {conditions if conditions else '-'}\n")
                f.write(f"   Columns:       {columns if columns else '-'}\n")
                f.write(f"   Rows affected: {rows_affected if rows_affected is not None else '-'}\n")
                f.write(f"   Details:       {details if details else '-'}\n\n")

        print(f"Audit log saved to: {out_path}")

    except Exception as e:
        print(f"Could not save audit log: {e}")