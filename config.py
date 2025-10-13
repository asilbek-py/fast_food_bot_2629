import dotenv
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = list(map(int, os.getenv("ADMIN_ID", "").split(",")))
