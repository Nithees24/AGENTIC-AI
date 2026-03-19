from llm.llm_client import LLMClient
from agents.general_chat_agent import GeneralChatAgent
from pipeline.planner import Planner


def main():
    llm_client = LLMClient()

    planner = Planner(llm_client)
    general_agent = GeneralChatAgent(llm_client)

    while True:

        user_query = input("\nUser:")

        plan = planner.plan(user_query)

        print("\n[Planner Output]:", plan)

        mode = plan.get("mode")

        if mode == "normal":
            response = general_agent.run(user_query)

        elif mode == "deep_research":
            response = "Deep research agent not implemented yet"

        else:
            response = "Planner failed"

        print("\nAI:", response)


if __name__ == "__main__":
    main()