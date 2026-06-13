from model import generate

def route_query(user_input):

    prompt = f"""
You are a medical routing system.

Classify the query into one of these:
- symptom
- emergency
- drug
- doctor
- general

User query: {user_input}

Return ONLY one word.
"""

    result = generate(prompt, 10).lower()

    if "emergency" in result:
        return "emergency"
    elif "symptom" in result:
        return "symptom"
    elif "drug" in result or "medicine" in result:
        return "drug"
    elif "doctor" in result:
        return "doctor"
    else:
        return "general"