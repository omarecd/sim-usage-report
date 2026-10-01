import sqlite3
from datetime import date

DB_PATH = "sim_usage.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sims (
            iccid TEXT PRIMARY KEY,
            label TEXT,
            organization TEXT,
            first_activation_date TEXT,
            quota_mb INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iccid TEXT,
            period_start TEXT,
            period_end TEXT,
            usage_kb INTEGER,
            FOREIGN KEY (iccid) REFERENCES sims (iccid),
            UNIQUE (iccid, period_start, period_end)
        )
    """)

    conn.commit()
    conn.close()


def save_sim(sim):
    """Insert or update a SIM's details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO sims (iccid, label, organization, first_activation_date, quota_mb)
        VALUES (?, ?, ?, ?, ?)
    """, (sim.iccid, sim.label, sim.organization, str(sim.first_activation_date), sim.quota_mb))
    conn.commit()
    conn.close()


def save_usage_record(record):
    """Insert one usage row."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO usage_records (iccid, period_start, period_end, usage_kb)
        VALUES (?, ?, ?, ?)
    """, (record.iccid, str(record.period_start), str(record.period_end), record.usage_kb))
    conn.commit()
    conn.close()