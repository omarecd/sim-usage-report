from dataclasses import dataclass
from datetime import date

@dataclass
class Sim:
    iccid: str
    label: str
    organization: str
    first_activation_date: date
    quota_mb: int


@dataclass
class UsageRecord:
    iccid: str
    period_start: date
    period_end: date
    usage_kb: int