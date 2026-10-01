from datetime import date, datetime
from sim_usage.api_client import get_sim_details, generate_usage_report, fetch_report_data
from sim_usage.transform import sum_usage_kb, kb_to_mb, percent_used, remaining_mb
from sim_usage.models import Sim, UsageRecord
from sim_usage.database import init_db, save_sim, save_usage_record
from sim_usage.config import QUOTA_MB


def process_sim(iccid: str):
    """Fetch, transform, and store usage data for one SIM."""

    # 1. Get SIM details
    details = get_sim_details(iccid)
    activation_date = details["dates"]["firstActivationDate"].split("T")[0]

    sim = Sim(
        iccid=details["iccid"],
        label=details["label"],
        organization=details.get("organization", "Unknown"),
        first_activation_date=date.fromisoformat(activation_date),
        quota_mb=QUOTA_MB
    )
    save_sim(sim)

    # 2. Pull usage since activation, up to today
    today = datetime.now().strftime("%Y-%m-%d 00:00:00")
    start = f"{activation_date} 00:00:00"

    report = generate_usage_report(iccid, start, today)
    rows = fetch_report_data(report["downloadUrl"])

    # 3. Save each monthly row, and print a summary
    for row in rows:
        record = UsageRecord(
            iccid=row["ICCID"],
            period_start=date.fromisoformat(row["Start Date"].split(" ")[0]),
            period_end=date.fromisoformat(row["End Date"].split(" ")[0]),
            usage_kb=int(row["Total Usage"])
        )
        save_usage_record(record)

    total_kb = sum_usage_kb(rows)
    total_mb = kb_to_mb(total_kb)

    print(f"\n--- {sim.label} ({sim.iccid}) ---")
    print(f"Total usage since activation: {total_mb} MB")
    print(f"Quota: {QUOTA_MB} MB")
    print(f"Used: {percent_used(total_mb, QUOTA_MB)}%")
    print(f"Remaining: {remaining_mb(total_mb, QUOTA_MB)} MB")


if __name__ == "__main__":
    init_db()
    process_sim("8944474400001330935")