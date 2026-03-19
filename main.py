from agents.deep_research_agent import DeepResearchAgent
from llm.llm_client import LLMClient
from pipeline.planner import Planner
from agents.general_chat_agent import GeneralChatAgent


def main():
    llm_client = LLMClient()
    planner = Planner(llm_client)
    agent = GeneralChatAgent(llm_client)

    while True:
        try:
            user_query =  input("\nUser:")
            if user_query.lower() in ["exit", "quit"]:
                break

            plan = planner.plan(user_query)

            print("\n🧠Plan:\n", plan)
            mode = plan["mode"]

            # Step 2: Route
            if mode == "normal":
                response = GeneralChatAgent.run(user_query, plan)

            elif mode == "deep_research":
                response = DeepResearchAgent.run(user_query, plan)

            else:
                response = "Invalid mode from planner"

            print("\n🤖AI:",response)

        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()