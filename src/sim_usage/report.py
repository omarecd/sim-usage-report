import csv
from datetime import date
from sim_usage.database import get_connection
from sim_usage.transform import kb_to_mb


def get_usage_rows():
    """Pull one row per (SIM, month) joined with the SIM's label."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.iccid, s.label, u.usage_kb
        FROM usage_records u
        JOIN sims s ON s.iccid = u.iccid
        ORDER BY s.label
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def build_report_rows():
    """Aggregate all months into one row per SIM: total usage since activation,
    plus the average monthly usage (total divided by number of months on record)."""
    totals_kb = {}
    month_counts = {}
    sim_info = {}

    for iccid, label, usage_kb in get_usage_rows():
        totals_kb[iccid] = totals_kb.get(iccid, 0) + usage_kb
        month_counts[iccid] = month_counts.get(iccid, 0) + 1
        sim_info[iccid] = label

    report_rows = []
    for iccid, total_kb in totals_kb.items():
        label = sim_info[iccid]
        total_mb = kb_to_mb(total_kb)
        months = month_counts[iccid]
        avg_monthly_mb = round(total_mb / months, 2)

        report_rows.append({
            "iccid": iccid,
            "label": label,
            "avg_monthly_usage_mb": avg_monthly_mb,
            "total_usage_mb": total_mb,
        })

    report_rows.sort(key=lambda r: r["label"])
    return report_rows


def default_report_filename() -> str:
    """Build today's report filename, e.g. teltonika_sims_usage_report_2026-10-06.csv"""
    return f"teltonika_sims_usage_report_{date.today().isoformat()}.csv"


def write_csv_report(path: str = None):
    """Write one row per SIM — total aggregated usage — to a CSV file.
    Defaults to a date-stamped filename generated at call time, not at import time."""
    if path is None:
        path = default_report_filename()

    rows = build_report_rows()

    fieldnames = ["iccid", "label", "avg_monthly_usage_mb", "total_usage_mb"]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return path


if __name__ == "__main__":
    out_path = write_csv_report()
    print(f"Report written to {out_path}")