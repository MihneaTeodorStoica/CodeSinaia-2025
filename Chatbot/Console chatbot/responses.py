import random

R_Eating = ["I don't like eating.", "I run on code, not food!", "Bots don't need to eat 😄"]

def get_custom_response(topic):
    if topic == "eat":
        return random.choice(R_Eating)
    return "Hmm... I don't know how to respond to that."

def unknown():
    responses = [
        "Could you please rephrase that?",
        "Hmm... I didn't quite get that.",
        "What does that mean? 🤔",
        "I'm not sure I understand."
    ]
    return random.choice(responses)