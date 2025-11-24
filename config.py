import os

# Pode alterar aqui, se preferir:
BASE_URL = os.environ.get("VIAGENS_API_URL", "http://localhost:3000").rstrip("/")

HEADERS = {
    "Content-Type": "application/json"
}
