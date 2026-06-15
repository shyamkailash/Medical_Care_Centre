from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()


def quick_medical_response(user_input):
    text = user_input.lower()

    if "fever" in text:
        return (
            "Fever may be due to infection, dehydration, or tiredness. "
            "Drink plenty of water, take rest, and monitor your temperature. "
            "Consult a doctor if the fever is high, lasts more than 2 days, or you feel very weak."
        )

    if "breath" in text or "breathing" in text or "chest pain" in text:
        return (
            "This may be serious. Please seek immediate medical help or contact emergency services, "
            "especially if breathing difficulty or chest pain is severe."
        )

    if "cough" in text or "cold" in text:
        return (
            "Cold and cough are commonly caused by viral infections or allergies. "
            "Drink warm fluids, rest well, and avoid cold exposure. "
            "See a doctor if symptoms worsen or continue for several days."
        )

    if "headache" in text:
        return (
            "Headache may happen due to stress, dehydration, lack of sleep, or fever. "
            "Drink water, rest in a quiet place, and monitor your symptoms. "
            "Consult a doctor if the pain is severe or repeated."
        )

    return None


def chat(user_input):
    quick_reply = quick_medical_response(user_input)
    if quick_reply:
        return quick_reply

    messages = [
        {
            "role": "system",
            "content": (
                "You are a real-time AI medical assistant. "
                "Reply directly to the user's health question. "
                "Do not create example conversations. "
                "Do not write User, Bot, Patient, Doctor, or Assistant labels. "
                "Do not diagnose disease. "
                "Give short, safe, practical advice in 2 to 3 sentences. "
                "If symptoms are serious, advise immediate medical help."
            ),
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=70,
            do_sample=False,
            repetition_penalty=1.2,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    stop_words = [
        "User:",
        "Bot:",
        "Assistant:",
        "Patient:",
        "Doctor:",
        "Example conversation:",
        "Conversation:"
    ]

    for word in stop_words:
        if word in response:
            response = response.split(word)[0].strip()

    if not response:
        response = "Please describe your symptoms clearly."

    return response


if __name__ == "__main__":
    print("\nAI Medical Chatbot Started\n")

    while True:
        user = input("You: ")

        if user.lower() in ["exit", "quit"]:
            print("Bot: Take care!")
            break

        print("Bot:", chat(user))