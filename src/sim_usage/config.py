import os
from dotenv import load_dotenv

load_dotenv()

TRUPHONE_API_TOKEN = os.getenv("TRUPHONE_API_TOKEN")
TRUPHONE_BASE_URL = "https://iot.truphone.com/api/v2.0"
QUOTA_MB = 500