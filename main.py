from twilio.rest import Client
from dotenv import load_dotenv
import os
import pandas as pd
from groq import Groq
import datetime
import requests

load_dotenv()

twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth = os.getenv("TWILIO_ACCOUNT_AUTH")
groq_api_key = os.getenv("GROQ_API_KEY")
tele_api_key = os.getenv("TELEGRAM_BOT")
whatsapp_number = os.getenv("WHATSAPP_NUMBER")
URL = f"https://api.telegram.org/bot{tele_api_key}/getUpdates"
SEND_URL = f"https://api.telegram.org/bot{tele_api_key}/sendMessage"


df = pd.read_csv("Vince's GRE Vocab Compilation and Curation - The Words.csv", usecols=["Vocab Cartoons App"])
extract_word = df["Vocab Cartoons App"].sample(n=3).tolist()


connect = Groq(api_key=groq_api_key)
prompt = f"For the following words explain the meaning and then use it in a casual sentence: {extract_word}"
try:
    completion = connect.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )
    messages = ""
    for chunk in completion:
        messages += chunk.choices[0].delta.content or ""
    messages = messages.strip()
    if len(messages) > 4000:
        messages = messages[:4000] + "..."
except Exception as e:
    print("Error with Groq API:", e)
    messages = "Failed to generate message"


try:
    client = Client(twilio_sid, twilio_auth)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=messages,
        to=f'whatsapp:+{whatsapp_number}'
    )
    with open("sent_messages_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {extract_word} → {messages[:100]}...\n")
except Exception as e:
    print("Error sending WhatsApp message:", e)

def update_chat_ids():
    response = requests.get(URL)
    updates = response.json()
    new_ids = set()
    removed_ids = set()

    if not os.path.exists("chat_ids.txt"):
        with open("chat_ids.txt", "w"): pass

    with open("chat_ids.txt", "r") as f:
        saved_ids = set(line.strip() for line in f if line.strip())

    for update in updates.get("result", []):
        try:
            msg = update["message"]
            chat_id = str(msg["chat"]["id"])
            text = msg.get("text", "").strip().lower()

            if text == "/start":
                new_ids.add(chat_id)
                send_message(chat_id, "✅ Subscribed to daily vocab messages! Send /stop to unsubscribe.")
            elif text == "/stop":
                removed_ids.add(chat_id)
                send_message(chat_id, "❌ Unsubscribed from vocab messages.")
        except Exception as e:
            print("Error reading update:", e)

    updated_ids = (saved_ids | new_ids) - removed_ids
    with open("chat_ids.txt", "w") as f:
        for cid in updated_ids:
            f.write(f"{cid}\n")


def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(SEND_URL, data=payload)

def broadcast_message(text):
    if not os.path.exists("chat_ids.txt"):
        return
    with open("chat_ids.txt", "r") as f:
        for chat_id in f:
            send_message(chat_id.strip(), text)


update_chat_ids()
broadcast_message(messages)
