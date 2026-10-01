import requests
from sim_usage.config import TRUPHONE_API_TOKEN, TRUPHONE_BASE_URL

HEADERS = {
    "Authorization": f"Bearer {TRUPHONE_API_TOKEN}",
    "Content-Type": "application/json"
}


def get_sim_details(iccid: str) -> dict:
    """Fetch a single SIM's details (label, org, activation date, etc.)."""
    response = requests.get(f"{TRUPHONE_BASE_URL}/sims/{iccid}/", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def generate_usage_report(iccid: str, start_date: str, end_date: str) -> dict:
    """Request a monthly DATA_USAGE report for one SIM over a date range."""
    payload = {
        "report_type": "DATA_USAGE",
        "iccid": [iccid],
        "granularity": "Month",
        "startDate": start_date,
        "endDate": end_date,
        "output_format": "JSON"
    }
    response = requests.post(f"{TRUPHONE_BASE_URL}/reports/generate", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def fetch_report_data(download_url: str) -> list:
    """Fetch the actual usage rows from the downloadUrl returned above."""
    response = requests.get(download_url, headers=HEADERS)
    response.raise_for_status()
    return response.json()