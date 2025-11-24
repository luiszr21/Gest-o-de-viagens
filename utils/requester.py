import requests
from config import BASE_URL, HEADERS

def api_request(method, path, params=None, json_body=None):
    url = f"{BASE_URL}/{path.lstrip('/')}"
    try:
        response = requests.request(
            method,
            url,
            headers=HEADERS,
            params=params,
            json=json_body,
            timeout=10
        )
    except requests.RequestException as e:
        print("Erro ao conectar à API:", e)
        return None

    try:
        data = response.json()
    except:
        data = response.text

    if response.status_code >= 400:
        print(f"Erro {response.status_code} -> {data}")
        return None

    return data
