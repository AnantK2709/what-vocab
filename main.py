import twilio
from twilio.rest import Client
from dotenv import load_dotenv
import os
import csv
import pandas as pd
import random
from groq import Groq
import datetime
import schedule

load_dotenv()

twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth = os.getenv("TWILIO_ACCOUNT_AUTH")
groq_api_key = os.getenv("GROQ_API_KEY")

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
    to='whatsapp:+917777078154'
    )
    with open("sent_messages_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {extract_word} → {messages[:100]}...\n")

except Exception as e:
    print("Error with Twilio API:", e)
