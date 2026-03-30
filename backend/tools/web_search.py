class WebSearch:
    def __init__(self):
        pass

    def search(self, query):
        print(f"[WebSearch] Searching for: {query}")

        # Mock results (Phase 1)
        return [
            {
                "title": "Sample Article 1",
                "url": "https://example.com/article1"
            },
            {
                "title": "Sample Article 2",
                "url": "https://example.com/article2"
            },
            {
                "title": "Sample Article 3",
                "url": "https://example.com/article3"
            }
        ]