from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

class WebSearch:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query):
        print(f"[WebSearch] Searching for: {query}")

        try:
            response = self.client.search(
                query=query,
                max_results=5
            )

            results = response.get("results", [])

            return [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "content": r.get("content", "")
                }
                for r in results
            ]

        except Exception as e:
            print(f"[WebSearch ERROR]: {e}")
            return []