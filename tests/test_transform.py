from sim_usage.transform import sum_usage_kb, kb_to_mb, percent_used, remaining_mb

# Real rows pulled from the API on 2026-10-01 — SIM 8944474400001330935 (Omar - FTC880)
real_rows = [
    {"Total Usage": "9249", "Start Date": "2026-06-01", "End Date": "2026-06-30", "ICCID": "8944474400001330935"},
    {"Total Usage": "9168", "Start Date": "2026-07-01", "End Date": "2026-07-31", "ICCID": "8944474400001330935"},
    {"Total Usage": "13845", "Start Date": "2026-08-01", "End Date": "2026-08-31", "ICCID": "8944474400001330935"},
    {"Total Usage": "6165", "Start Date": "2026-09-01", "End Date": "2026-09-30", "ICCID": "8944474400001330935"},
]


def test_sum_usage_kb():
    assert sum_usage_kb(real_rows) == 38427


def test_sum_usage_kb_empty():
    assert sum_usage_kb([]) == 0


def test_kb_to_mb():
    assert kb_to_mb(38427) == 37.53


def test_percent_used():
    assert percent_used(37.53, 500) == 7.51


def test_remaining_mb():
    assert remaining_mb(37.53, 500) == 462.47