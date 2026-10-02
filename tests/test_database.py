import os
import pytest
from sim_usage import database
from sim_usage.models import Sim, UsageRecord
from datetime import date


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point database.py at a temporary file instead of the real database."""
    test_db_path = tmp_path / "test_sim_usage.db"
    monkeypatch.setattr(database, "DB_PATH", str(test_db_path))
    database.init_db()
    yield test_db_path


def test_save_usage_record_no_duplicates(temp_db):
    record = UsageRecord(
        iccid="123",
        period_start=date(2026, 6, 1),
        period_end=date(2026, 6, 30),
        usage_kb=1000
    )

    database.save_usage_record(record)
    database.save_usage_record(record)  # insert the SAME record twice

    conn = database.get_connection()
    count = conn.execute("SELECT COUNT(*) FROM usage_records").fetchone()[0]
    conn.close()

    assert count == 1  # must still be 1, not 2


def test_save_usage_record_updates_value(temp_db):
    record_v1 = UsageRecord(iccid="123", period_start=date(2026, 6, 1), period_end=date(2026, 6, 30), usage_kb=1000)
    record_v2 = UsageRecord(iccid="123", period_start=date(2026, 6, 1), period_end=date(2026, 6, 30), usage_kb=2000)

    database.save_usage_record(record_v1)
    database.save_usage_record(record_v2)  # same SIM+month, different usage

    conn = database.get_connection()
    row = conn.execute("SELECT usage_kb FROM usage_records").fetchone()
    conn.close()

    assert row[0] == 2000  # latest value wins, old one replaced


def test_save_sim_upsert(temp_db):
    sim_v1 = Sim(iccid="123", label="Old Label", organization="ALSO", first_activation_date=date(2026, 1, 1), quota_mb=500)
    sim_v2 = Sim(iccid="123", label="New Label", organization="ALSO", first_activation_date=date(2026, 1, 1), quota_mb=500)

    database.save_sim(sim_v1)
    database.save_sim(sim_v2)

    conn = database.get_connection()
    count = conn.execute("SELECT COUNT(*) FROM sims").fetchone()[0]
    label = conn.execute("SELECT label FROM sims").fetchone()[0]
    conn.close()

    assert count == 1
    assert label == "New Label"