import json
import os
from datetime import datetime
import requests

DATA_FILE = "data.json"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"   # change to gemma3:27b if you want, but it will be slower


# -------------------------
# Data helpers
# -------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_entry(entry):
    data = load_data()
    data.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -------------------------
# Fast analytics (no LLM)
# -------------------------
def classify_intent(message: str) -> str:
    m = message.lower()
    if any(x in m for x in ["price", "cost", "pricing", "plan", "subscription", "monthly", "yearly"]):
        return "pricing"
    if any(x in m for x in ["demo", "book", "schedule", "call", "meeting", "trial"]):
        return "demo_request"
    if any(x in m for x in ["error", "issue", "problem", "not working", "can't log in", "cannot log in", "bug"]):
        return "support"
    if any(x in m for x in ["cancel", "refund", "leaving", "stop using", "unhappy", "not happy"]):
        return "complaint"
    return "general_enquiry"


def classify_sentiment(message: str) -> str:
    m = message.lower()
    if any(x in m for x in ["love", "great", "amazing", "awesome", "perfect", "thanks", "thank you"]):
        return "positive"
    if any(x in m for x in ["angry", "upset", "hate", "terrible", "horrible", "worst", "not happy", "unhappy"]):
        return "negative"
    if any(x in m for x in ["not working", "error", "issue", "problem", "can't", "cannot"]):
        return "negative"
    return "neutral"


def lead_score(intent: str, sentiment: str) -> int:
    base = {
        "demo_request": 90,
        "pricing": 75,
        "support": 40,
        "general_enquiry": 30,
        "complaint": 10
    }
    score = base.get(intent, 20)
    if sentiment == "positive":
        score += 10
    elif sentiment == "negative":
        score -= 20
    return max(0, min(score, 100))


def recommended_action(intent: str, score: int) -> str:
    if score >= 80:
        return "Assign to sales immediately and offer a quick demo slot."
    if score >= 60:
        return "Send pricing details and a relevant case study. Offer a short call."
    if score >= 40:
        return "Share support resources and follow up if unresolved."
    if score >= 20:
        return "Add to nurture and monitor engagement."
    return "Low priority. No immediate follow-up."


# -------------------------
# Ollama chat call (keeps history)
# -------------------------
def ollama_chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]


def main():
    print("\nOllama Chat Logger ✅")
    print("Type your message. Type /exit to quit.\n")

    # chat history for Ollama context
    messages = [
        {"role": "system", "content": "You are a helpful customer support agent for a SaaS product. Be concise and human."}
    ]

    while True:
        user_msg = input("You: ").strip()
        if not user_msg:
            continue
        if user_msg.lower() in ["/exit", "exit", "quit"]:
            print("Bye.")
            break

        # 1) Log analytics for USER message (this feeds your dashboard)
        intent = classify_intent(user_msg)
        sentiment = classify_sentiment(user_msg)
        score = lead_score(intent, sentiment)
        action = recommended_action(intent, score)

        save_entry({
            "timestamp": str(datetime.now()),
            "message": user_msg,
            "intent": intent,
            "sentiment": sentiment,
            "lead_score": score,
            "recommended_action": action
        })

        # 2) Get Ollama reply (real chat)
        messages.append({"role": "user", "content": user_msg})
        try:
            reply = ollama_chat(messages)
        except Exception as e:
            reply = f"(Oallow) Error talking to Ollama: {e}"

        messages.append({"role": "assistant", "content": reply})
        print(f"\nAgent: {reply}\n")


if __name__ == "__main__":
    main()
