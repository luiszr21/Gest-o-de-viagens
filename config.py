import os

BASE_URL = os.environ.get("VIAGENS_API_URL", "http://localhost:3000").rstrip("/")

HEADERS = {
    "Content-Type": "application/json"
}
