from tools.scrapper import Scrapper
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

    def __init__(self):
        self.llm = llm_client

        #pipeline
        self.planner = Planner()
        self.synthesizer = Synthesizer()
        self.ranker = Ranker()
        self.aggregator = Aggregator()

        #tools
        self.paper_fetch = PaperFetch()
        self.web_search = WebSearch()
        self.scraper = Scrapper()
        self.pdf_parser = PDFParser()

        #control
        self.max_urls_per_query = 3
        self.max_docs_after_ranking = 5

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



