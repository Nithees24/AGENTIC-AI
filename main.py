from llm.llm_client import LLMClient
from agents.general_chat_agent import GeneralChatAgent


def main():
    llm_client = LLMClient()

    agent = GeneralChatAgent(llm_client)

    while True:

        user_query =  input("\nUser:")

        response = agent.run(user_query)

        print("\nAI:",response)
        #printing response

if __name__ == "__main__":
    main()