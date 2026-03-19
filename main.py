from llm.llm_client import LLMClient
from pipeline.planner import Planner
from agents.general_chat_agent import GeneralChatAgent


def main():
    llm_client = LLMClient()
    planner = Planner(llm_client)
    agent = GeneralChatAgent(llm_client)

    while True:

        user_query =  input("\nUser:")

        plan = planner.plan(user_query)
        print("\n🧠Plan:\n", plan)

        response = agent.run(user_query)
        print("\n🤖AI:",response)


if __name__ == "__main__":
    main()