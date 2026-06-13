from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# ✅ ADD THIS
SYSTEM_PROMPT = """
You are a helpful medical assistant chatbot.

Rules:
- Do NOT give final diagnosis
- Understand user symptoms clearly
- Ask follow-up questions
- Suggest simple precautions
- Warn for serious symptoms

Keep answers short and structured.
"""

def chat(user_input):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(input_text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "<|assistant|>" in full_output:
        response = full_output.split("<|assistant|>")[-1]
    else:
        response = full_output

    return response.strip()


while True:
    user = input("You: ")
    print("Bot:", chat(user))