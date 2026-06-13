from model import generate

def emergency_agent(user_input):
    prompt = f"""
You are an emergency detection system.

If symptoms are severe (chest pain, breathing issues, unconsciousness),
you MUST recommend immediate medical attention.

User: {user_input}
"""

    return generate(prompt, 200)