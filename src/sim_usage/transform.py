def sum_usage_kb(rows: list[dict]) -> int:
    """Sum the 'Total Usage' field (in KB) across a list of usage rows."""
    return sum(int(row["Total Usage"]) for row in rows)


def kb_to_mb(kb: int) -> float:
    """Convert KB to MB, rounded to 2 decimal places."""
    return round(kb / 1024, 2)


def percent_used(usage_mb: float, quota_mb: int) -> float:
    """Percentage of quota consumed."""
    return round((usage_mb / quota_mb) * 100, 2)


def remaining_mb(usage_mb: float, quota_mb: int) -> float:
    """MB remaining out of quota."""
    return round(quota_mb - usage_mb, 2)