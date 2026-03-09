import requests

LIVE_CLIENT_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

def get_live_data():
    try:
        response = requests.get(LIVE_CLIENT_URL, verify=False)
        return response.json()
    except Exception:
        return {}