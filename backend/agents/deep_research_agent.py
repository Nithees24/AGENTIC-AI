from tools.scraper import Scraper
from tools.paper_fetch import PaperFetch
from tools.pdf_parser import PDFParser
from tools.web_search import WebSearch
from pipeline.ranker import Ranker
from pipeline.synthesizer import Synthesizer
from pipeline.aggregator import Aggregator
from pipeline.planner import Planner


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

        # tools
        self.paper_fetch = PaperFetch()
        self.web_search = WebSearch()
        self.scraper = Scraper()
        self.pdf_parser = PDFParser()

    def run(self, user_query:str)->str:
        try:
            questions = self._plan(user_query)
            web_docs = self._search_and_scrape(questions)
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

    def _search_and_scrape(self, questions):
        docs = []
        print("[2] Web search + scraping...")

        for q in questions:
            try:
                results = self.web_search.search(q)
            except Exception as e:
                print(f"Search failed for '{q}': {e}")
                continue

            for r in results[:self.max_urls_per_query]:
                url = r.get("url")
                if not url:
                    continue

                try:
                    doc = self.scraper.scrape(url)
                    if doc and doc.get("content"):
                        doc["source"] = "web"
                        docs.append(doc)
                except Exception as e:
                    print(f"Scraping failed for {url}: {e}")

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
