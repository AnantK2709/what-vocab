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
URL = f"https://api.telegram.org/bot{tele_api_key}/getUpdates"
whatsapp_number = os.getenv("WHATSAPP_NUMBER")

df = pd.read_csv("Vince's GRE Vocab Compilation and Curation - The Words.csv", usecols=["Vocab Cartoons App"])
extract_word = df["Vocab Cartoons App"].sample(n=3).tolist()


connect = Groq(api_key=groq_api_key)
message = f"For the following words explain the meaning and then use it in a casual sentence {extract_word}"
try: 
    completion = connect.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
        {
            "role": "user",
            "content":  message   
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
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


client = Client(twilio_sid, twilio_auth)
try:
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body = messages,
    to=f'whatsapp:+{whatsapp_number}'
    )
    with open("sent_messages_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {extract_word} → {messages[:100]}...\n")
except Exception as e:
    print("Error with Twilio API:", e)

def get_chat_ids():
    response = requests.get(URL)
    updates = response.json()
    chat_ids = set()

    for update in updates.get("result", []):
        chat_id = update["message"]["chat"]["id"]
        chat_ids.add(chat_id)

    return list(chat_ids)

chat_ids = get_chat_ids()
with open("chat_ids.txt", "w") as f:
    for cid in chat_ids:
        f.write(f"{cid}\n")

def broadcast_message(text):
    with open("chat_ids.txt", "r") as f:
        chat_ids = [line.strip() for line in f.readlines()]

    for chat_id in chat_ids:
        send_url = f"https://api.telegram.org/bot{tele_api_key}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(send_url, data=payload)
broadcast_message(messages)
