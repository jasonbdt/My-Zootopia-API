from typing import Any
import os

from dotenv import load_dotenv
import requests

load_dotenv()

API_BASE = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")

def get_animal(name: str) -> dict[str, Any]:
    return requests.get(API_BASE, {
        "name": name.lower()
    }, headers={
        "X-Api-Key": API_KEY
    }).json()
