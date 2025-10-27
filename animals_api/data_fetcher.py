from typing import Any, Optional
import os

from dotenv import load_dotenv
import requests
load_dotenv()

API_BASE = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")

def fetch_data(animal_name: str) -> Optional[list[dict[str, Any]]]:
    response = requests.get(API_BASE, {
        "name": animal_name.lower()
    }, headers={
        "X-Api-Key": API_KEY
    })

    if response.ok:
        return response.json()

    return None
