import json
from datetime import datetime, timedelta
import random

def generate_simulated_chat(path="C:\\Users\\palak\\PycharmProjects\\Android and OSINT analysis\\chat_analysis\\example_logs\\chat.json"):
    names = ["Raj", "Neha", "Amit", "Officer Kumar", "Agent007"]

    # More diverse and Hinglish messages
    templates = [
        "Bhai kal wali *govt report* bhejna mat bhoolna",
        "Woh *confidential file* ka kya hua?",
        "Yeh document kisi ko mat dikhana plz",
        "Arey sir, yeh toh *leak* ho gaya!",
        "Mujhe kal ek *password protected file* mili thi from server",
        "Tu mere se mil, kuch *classified cheez* hai batani",
        "Aaj raat tak *doc123.pdf* bhej dena",
        "Wahi purani wali file with *govt logo* mila kya?",
        "Yeh *budget_summary.xlsx* media mein leak ho gaya kya?",
        "Apna kaam ho gaya kya with *contract_final.docx*?"
    ]

    start_time = datetime.now() - timedelta(days=1)
    messages = []

    for i in range(50):
        sender = random.choice(names)
        message = random.choice(templates)
        timestamp = (start_time + timedelta(minutes=12*i)).strftime("%Y-%m-%d %H:%M:%S")
        messages.append({
            "sender": sender,
            "timestamp": timestamp,
            "message": message
        })

    with open(path, "w") as f:
        json.dump(messages, f, indent=2)

# Run to generate
if __name__ == "__main__":
    generate_simulated_chat()
