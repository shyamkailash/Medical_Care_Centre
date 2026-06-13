def medical_prompt(user_query: str, context: str = ""):
    return f"""
You are a helpful medical assistant.
Provide safe, general medical advice only.

Context:
{context}

User Query:
{user_query}

Response:
"""