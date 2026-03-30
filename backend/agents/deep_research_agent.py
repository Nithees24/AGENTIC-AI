from backend.tools.scraper import Scraper
from backend.tools.paper_fetch import PaperFetch
from backend.tools.pdf_parser import PDFParser
from backend.tools.web_search import WebSearch
from backend.pipeline.ranker import Ranker
from backend.pipeline.synthesizer import Synthesizer
from backend.pipeline.aggregator import Aggregator
from backend.pipeline.planner import Planner
from backend.pipeline.query_generator import QueryGenerator


class DeepResearchAgent:
    """
       Orchestrates the full deep research pipeline:
       Plan → Search → Scrape → Fetch Papers → Parse PDFs → Rank → Summarize → Aggregate
    """

    def __init__(self, llm_client):
        self.llm = llm_client

        # pipeline
        self.planner = Planner(llm_client)
        self.synthesizer = Synthesizer(llm_client)
        self.ranker = Ranker()
        self.aggregator = Aggregator(llm_client)
        self.query_generator = QueryGenerator(self.llm)

        # tools
        self.paper_fetch = PaperFetch()
        self.web_search = WebSearch()
        self.scraper = Scraper()
        self.pdf_parser = PDFParser()


    def run(self, user_query:str)->str:
        try:
            queries  = self.query_generator.generate(user_query)
            web_docs = self._search_and_scrape(queries)
            paper_docs = self._fetch_and_parse_papers(user_query)

            all_docs = web_docs + paper_docs

            if not all_docs:
                return "No relevant data found."

            ranked_docs = self._rank(all_docs)
            summaries = self._summarize(ranked_docs)

            if not summaries:
                return "Failed to generate summaries."

            return self._aggregate(user_query, summaries)

        except Exception as e:
            print(f"[FATAL ERROR]: {e}")
            return "Something went wrong during deep research."

    # -----------------------------
    # Individual Steps
    # -----------------------------

    def _plan(self, query):
        try:
            print("[1] Planning...")
            plan = self.planner.plan(query)
            return plan.get("steps", [])
        except Exception as e:
            print(f"Planner error: {e}")
            return []

    def _search_and_scrape(self, user_query):
        docs = []
        print("[2] Web search + scraping...")

        # Generate queries
        try:
            queries = self.query_generator.generate(user_query)
        except Exception as e:
            print(f"[QueryGenerator ERROR]: {e}")
            return docs

        if not queries:
            print("[WARNING] No queries generated")
            return docs

        for q in queries:
            print(f"[SEARCH] Query: {q}")

            # --- Web Search ---
            try:
                results = self.web_search.search(q)
            except Exception as e:
                print(f"[Search ERROR] '{q}': {e}")
                continue

            if not results:
                print(f"[INFO] No results for query: {q}")
                continue

            # --- Limit URLs safely ---
            max_urls = getattr(self, "max_urls_per_query", 3)

            for r in results[:max_urls]:
                if not isinstance(r, dict):
                    continue

                url = r.get("url") or r.get("link")
                if not url:
                    continue

                print(f"[SCRAPE] {url}")

                # --- Scraping ---
                try:
                    doc = self.scraper.scrape(url)

                    if not doc or not isinstance(doc, dict):
                        continue

                    content = doc.get("content")
                    if not content:
                        continue

                    docs.append({
                        "title": doc.get("title", "Web Document"),
                        "content": content[:5000],  # prevent huge payloads
                        "source": "web",
                        "url": url
                    })

                except Exception as e:
                    print(f"[Scraper ERROR] {url}: {e}")
                    continue

        print(f"[DONE] Collected {len(docs)} documents")
        return docs

    def _fetch_and_parse_papers(self, query):
        docs = []
        print("[3] Paper fetch + parsing...")

        try:
            papers = self.paper_fetch.fetch(query)
        except Exception as e:
            print(f"Paper fetch failed: {e}")
            return docs

        for paper in papers:
            pdf_url = paper.get("pdf_url")
            if not pdf_url:
                continue

            try:
                text = self.pdf_parser.parse(pdf_url)
                if text:
                    docs.append({
                        "title": paper.get("title", "Research Paper"),
                        "content": text,
                        "source": "paper"
                    })
            except Exception as e:
                print(f"PDF parsing failed for {pdf_url}: {e}")

        return docs


    def _rank(self, documents):
        try:
            print("[4] Ranking...")
            ranked = self.ranker.rank(documents)
            return ranked[:self.max_docs_after_ranking]
        except Exception as e:
            print(f"Ranking error: {e}")
            return documents[:self.max_docs_after_ranking]

    def _summarize(self, documents):
        summaries = []
        print("[5] Summarizing...")

        for doc in documents:
            try:
                summary = self.synthesizer.summarize(doc)
                if summary:
                    summaries.append(summary)
            except Exception as e:
                print(f"Summarization failed: {e}")

        return summaries

    def _aggregate(self, query, summaries):
        try:
            print("[6] Aggregating final report...")
            return self.aggregator.aggregate(query, summaries)
        except Exception as e:
            print(f"Aggregation error: {e}")
            return "Failed to generate final report."
