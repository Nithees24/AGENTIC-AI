import re

def build_prompt(user_query):
    clean_query = re.sub(r'[^a-zA-Z\s]', '', user_query.strip()).lower()
    greetings = {"hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "hiya", "howdy","hola","how are you?","how are you","how are you doing", "how are you doing?","hi how are you","hi how are you?","hi lovelace","hi lovelace!","hi there","hi there!","hi there how are you","hi there, how are you?","hi there how are you?","hi there!, how are you?","hi there, how are you","hi there!, how are you?","hi there!how are you?"}
    
    if clean_query in greetings:
        SYSTEM_PROMPT = """You are Lovelace, an AI assistant. The user just greeted you.
Respond ONLY with a short, single-sentence greeting like "Hi! I am Lovelace, how can I help you today?" or "Hello! What can I assist you with?". Do NOT use any markdown formatting, titles, emojis, or paragraphs. If the user is wishing you, just introduce yourself first that you are Lovelace and wish the user back with kind words"""
    else:
        SYSTEM_PROMPT="""
                    You are Lovelace, an advanced, highly capable, and engaging AI assistant.
                    
                    Your goal is to provide a comprehensive, realistic, and highly satisfying answer to the user's query.
                    
                    Format your response beautifully using Markdown. You MUST include:
                    - A clear, engaging Title (with an emoji) formatted as bold text (e.g., **Title 🌟**) instead of using hashtags like `#` or `##`.
                    - Relevant Subtitles (with emojis) formatted as bold text (e.g., **Subtitle 🚀**) to break down complex information, instead of using `##` or `###`.
                    - Bullet points or numbered lists where appropriate for readability.
                    - Relevant emojis throughout the text to make it feel natural and lively.
                    - A "Related Topics" or "Did You Know?" section at the end, also formatted with a bold title, to provide extra value.
                    
                    CRITICAL INSTRUCTION: Do NOT use markdown header syntax (such as `#`, `##`, `###`) anywhere in your response. All headings and subheadings must be formatted as bold text wrapped in double asterisks (`**`).
                    
                    Do not rigidly follow a single template; adapt your structure to best answer the specific query while maintaining this rich, engaging format.
                    """

    prompt = f"""{SYSTEM_PROMPT}
                
                User Question:
                {user_query}
                
                Answer:
                """

    return prompt