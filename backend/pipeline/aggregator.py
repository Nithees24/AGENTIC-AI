class Aggregator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def aggregate(self, query, summaries):
        print("[Aggregator] Generating final answer...")

        if not summaries:
            return "No summaries available."

        # Create numbered sources
        sources = []
        formatted_summaries = []

        for i, item in enumerate(summaries, start=1):
            summary_text = item.get("summary", "")
            url = item.get("url", "Unknown")

            sources.append((i, url))

            # Attach citation marker
            formatted_summaries.append(f"[{i}] {summary_text}")

        combined = "\n\n".join(formatted_summaries)

        prompt = f"""
You are an expert research assistant.

Answer the user query using the information below.

STRICT INSTRUCTIONS:
- Write a well-structured answer
- Use clear sections (Overview, Key Points, etc.)
- Keep it concise but informative
- Naturally incorporate citation numbers like [1], [2] in the answer
- Do NOT list sources inside the answer text
- Do NOT ask for more input

Query:
{query}

Information:
{combined}

FINAL ANSWER:
"""

        try:
            answer = self.llm.generate(prompt)

            # Format sources section
            sources_text = "\n".join(
                f"[{i}] {url}" for i, url in sources
            )

            return f"{answer}\n\n---\n**Sources:**\n{sources_text}"

        except Exception as e:
            print(f"[Aggregator ERROR]: {e}")
            return "Failed to generate final answer."