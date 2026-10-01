import os
from dotenv import load_dotenv

load_dotenv()

TRUPHONE_API_TOKEN = os.getenv("TRUPHONE_API_TOKEN")
TRUPHONE_BASE_URL = "https://iot.truphone.com/api/v2.0"
TRUPHONE_BASE_URL_V2 = "https://iot.truphone.com/api/v2.0"
TRUPHONE_BASE_URL_V2_2 = "https://iot.truphone.com/api/v2.2"


QUOTA_MB = 500