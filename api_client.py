import requests
import json
import os
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# Konfiguration
CRCON_API_URL = os.getenv('CRCON_API_URL')
CRCON_API_KEY = os.getenv('CRCON_API_KEY')

HEADERS = {
    "Authorization": f"Bearer {CRCON_API_KEY}",
    "Content-Type": "application/json"
}

class APIClient:
    @staticmethod
    def send_request(endpoint: str, method: str = "GET", payload: dict = None):
        url = f"{CRCON_API_URL}/api/{endpoint}"
        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=HEADERS, json=payload)
            elif method.upper() == "GET":
                response = requests.get(url, headers=HEADERS)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Log response
            print(f"Statuscode: {response.status_code}")
            print(f"Antwort: {response.text}")
            response.raise_for_status()
            return response.json() if response.text.strip() else None
        except requests.exceptions.RequestException as e:
            print(f"HTTP-Fehler: {e}")
            return {"failed": True, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"JSON-Fehler: {e}")
            return {"failed": True, "error": str(e)}

    @staticmethod
    def clear_cache():
        """Leert den Cache des Servers."""
        return APIClient.send_request("clear_cache", method="POST", payload={})

    @staticmethod
    def apply_settings(settings: dict):
        """Wendet die Server-Einstellungen an."""
        payload = {"settings": json.dumps(settings)}
        return APIClient.send_request("set_auto_settings", method="POST", payload=payload)
        
    @staticmethod
    def get_auto_settings():
        """Holt die aktuell geladenen Autosettings vom Server."""
        return APIClient.send_request("get_auto_settings", method="GET")