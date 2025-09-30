from typing import Any
import requests

API_BASE = "https://api.api-ninjas.com/v1/animals"
API_KEY = "qoWNFWqBIRsslGC4k0EoDA==DuuApyPyQlGpXs8J"

def get_animal(name: str) -> dict[str, Any]:
    res = requests.get(API_BASE, {
        "name": name.lower()
    }, headers={
        "X-Api-Key": API_KEY
    }).json()

    print(res)
