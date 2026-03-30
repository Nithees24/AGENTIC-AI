class Aggregator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def aggregate(self, query, summaries):
        print("[Aggregator] Generating final answer...")

        if not summaries:
            return "No summaries available to generate answer."

        combined = "\n\n".join(summaries)

        prompt = f"""
You are an expert research assistant.

Using the information below, answer the user query.

STRICT INSTRUCTIONS:
- Do NOT ask for more input
- Provide a clear, structured answer
- Be concise but informative

User Query:
{query}

Information:
{combined}

FINAL ANSWER:
"""

        try:
            return self.llm.generate(prompt)
        except Exception as e:
            print(f"[Aggregator ERROR]: {e}")
            return "Failed to generate final answer."