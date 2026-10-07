import csv
import pytest
from datetime import date
from sim_usage import database, report
from sim_usage.models import Sim, UsageRecord


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point database.py at a temporary file instead of the real database."""
    test_db_path = tmp_path / "test_sim_usage.db"
    monkeypatch.setattr(database, "DB_PATH", str(test_db_path))
    database.init_db()
    yield test_db_path


def seed_two_months(iccid="123", label="Test SIM"):
    database.save_sim(Sim(
        iccid=iccid, label=label, organization="ALSO",
        first_activation_date=date(2026, 6, 1), quota_mb=500
    ))
    database.save_usage_record(UsageRecord(
        iccid=iccid, period_start=date(2026, 6, 1), period_end=date(2026, 6, 30), usage_kb=10240  # 10 MB
    ))
    database.save_usage_record(UsageRecord(
        iccid=iccid, period_start=date(2026, 7, 1), period_end=date(2026, 7, 31), usage_kb=20480  # 20 MB
    ))


def test_build_report_rows_one_row_per_sim(temp_db):
    seed_two_months()
    rows = report.build_report_rows()

    assert len(rows) == 1  # one row for this SIM, not one per month
    assert rows[0]["total_usage_mb"] == 30.0  # 10 + 20 MB aggregated


def test_build_report_rows_average_monthly(temp_db):
    seed_two_months()  # 10 MB + 20 MB across 2 months
    rows = report.build_report_rows()

    assert rows[0]["avg_monthly_usage_mb"] == 15.0  # 30 / 2 months


def test_build_report_rows_separates_sims(temp_db):
    seed_two_months(iccid="123", label="SIM A")
    seed_two_months(iccid="456", label="SIM B")

    rows = report.build_report_rows()

    assert len(rows) == 2
    totals = {r["iccid"]: r["total_usage_mb"] for r in rows}
    assert totals["123"] == 30.0
    assert totals["456"] == 30.0  # independent totals per SIM


def test_write_csv_report(temp_db, tmp_path):
    seed_two_months()
    out_path = tmp_path / "out.csv"
    report.write_csv_report(str(out_path))

    with open(out_path) as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1
    assert rows[0]["label"] == "Test SIM"
    assert rows[0]["total_usage_mb"] == "30.0"
    assert rows[0]["avg_monthly_usage_mb"] == "15.0"


def test_default_report_filename_format(monkeypatch):
    class FixedDate(date):
        @classmethod
        def today(cls):
            return date(2026, 10, 6)

    monkeypatch.setattr(report, "date", FixedDate)

    assert report.default_report_filename() == "teltonika_sims_usage_report_2026-10-06.csv"