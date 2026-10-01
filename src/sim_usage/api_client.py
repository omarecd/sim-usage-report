import requests
from sim_usage.config import TRUPHONE_API_TOKEN, TRUPHONE_BASE_URL_V2, TRUPHONE_BASE_URL_V2_2

HEADERS = {
    "Authorization": f"Token {TRUPHONE_API_TOKEN}",
    "Content-Type": "application/json"
}


def get_sim_details(iccid: str) -> dict:
    """Fetch a single SIM's details (label, org, activation date, etc.)."""
    response = requests.get(f"{TRUPHONE_BASE_URL_V2_2}/sims/{iccid}/", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_all_sims(per_page: int = 100) -> list:
    """Fetch all SIMs in the account."""
    response = requests.get(
        f"{TRUPHONE_BASE_URL_V2_2}/sims",
        headers=HEADERS,
        params={"per_page": per_page}
    )
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
    response = requests.post(f"{TRUPHONE_BASE_URL_V2}/reports/generate", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def fetch_report_data(download_url: str) -> list:
    """Fetch the actual usage rows from the downloadUrl returned above."""
    response = requests.get(download_url, headers=HEADERS)
    response.raise_for_status()
    return response.json()