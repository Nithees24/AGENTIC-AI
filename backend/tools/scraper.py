import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        pass

    def scrape(self, url):
        print(f"[Scraper] Scraping: {url}")

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"[Scraper ERROR] Status code: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract paragraphs
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text() for p in paragraphs)

            if not text.strip():
                return None

            return {
                "title": url,
                "content": text[:5000]  # limit size
            }

        except Exception as e:
            print(f"[Scraper ERROR]: {e}")
            return None