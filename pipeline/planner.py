class Planner:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def plan(self, user_query):
        prompt = self._build_planner_prompt(user_query)

        response = self.llm_client.generate(prompt)

        return response

    def _build_planner_prompt(self, user_query):
        return f"""
You are an intelligent planning agent.

Your job is to break down the user query into clear step-by-step actions.

Rules:
- Do NOT answer the question
- Only return a structured plan
- Keep steps logical and minimal

User Query:
{user_query}

Output Format:
1. Step 1
2. Step 2
3. Step 3
"""