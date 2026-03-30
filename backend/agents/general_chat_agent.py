from backend.utils.prompt_builder import build_prompt


class GeneralChatAgent:

    def __init__(self, llm_client):

        self.llm_client = llm_client

    def run(self, user_query):

        prompt = build_prompt(user_query)

        response = self.llm_client.generate(prompt)

        return response