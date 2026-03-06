from config import SYSTEM_PROMPT


def build_prompt(user_query):

    prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_query}

Answer:
"""

    return prompt