from backend.llm.llm_client import LLMClient
from backend.agents.general_chat_agent import GeneralChatAgent
from backend.agents.deep_research_agent import DeepResearchAgent
from backend.pipeline.planner import Planner

def main():
    llm_client = LLMClient()

    planner = Planner(llm_client)
    general_agent = GeneralChatAgent(llm_client)
    deep_agent = DeepResearchAgent(llm_client)

    while True:

        user_query = input("\nUser:")

        plan = planner.plan(user_query)

        print("\n[Planner Output]:", plan)

        mode = plan.get("mode")

        if mode == "normal":
            response = general_agent.run(user_query)

        elif mode == "deep_research":
            response = deep_agent.run(user_query)

        else:
            response = "Planner failed"

        print("\nAI:", response)


if __name__ == "__main__":
    main()