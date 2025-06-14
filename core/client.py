# fitgirl/client.py

import re
import httpx

from utils.config import get_config_value
from .parser import parse_search_results, parse_download_sections

BASE_URL = get_config_value(
    "FIT-GIRL-REPACKS-SETTINGS", "BASE_URL", fallback="https://fitgirl-repacks.site/"
)


class FitGirlClient:
    def check_status(self):
        try:
            response = httpx.get(BASE_URL, timeout=5.0)
            response.raise_for_status()
            return {"status": "Up", "code": response.status_code}
        except httpx.RequestError as e:
            return {"status": "Down", "message": str(e)}
        except httpx.HTTPStatusError as e:
            return {"status": "Error", "message": f"HTTP {e.response.status_code}"}

    def search(self, query):
        try:
            response = httpx.get(f"{BASE_URL}/?s={query}", timeout=10.0)
            response.raise_for_status()
            return parse_search_results(response.text)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def download_interactive(self, query):
        try:
            search_response = httpx.get(f"{BASE_URL}/?s={query}", timeout=10.0)
            search_response.raise_for_status()
            search_result = parse_search_results(search_response.text)
            if search_result["status"] != "Success":
                return search_result
            first_url = search_result["results"][0]["url"]
            title = search_result["results"][0]["title"]

            page_response = httpx.get(first_url, timeout=10.0)
            page_response.raise_for_status()
            sections = parse_download_sections(page_response.text)

            return {"status": "Success", "sections": sections, "title": title}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def new_posts(self):
        try:
            response = httpx.get(BASE_URL, timeout=10.0)
            response.raise_for_status()
            return parse_search_results(response.text, exclude_upcoming=True)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
