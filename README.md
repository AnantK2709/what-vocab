# 📚 Daily Vocab Bot — Telegram + WhatsApp

This project automates the daily sending of vocabulary messages to:
- ✅ Your WhatsApp (using Twilio)
- ✅ Telegram users who opt in by sending `/start`

Vocabulary is selected randomly from a curated dataset and explained using the **Groq API** with the `llama-4-scout-17b` model.

---

## 🚀 Features

- ✅ Sends 3 random vocab words daily at **9 AM IST**
- ✅ Groq LLM explains each word + gives a casual usage sentence
- ✅ Sends output to:
  - WhatsApp (your number via Twilio)
  - Telegram users who send `/start`
- ✅ Telegram users can unsubscribe by sending `/stop`
- ✅ Fully serverless — runs daily via **GitHub Actions**
- ✅ Easy to customize and extend

---

## 📁 Folder Structure

```

.
├── main.py                   # Main automation script
├── chat\_ids.txt              # Stores Telegram users who opted in
├── sent\_messages\_log.txt     # Optional log of messages sent
├── requirements.txt          # Python dependencies
└── .github/
└── workflows/
└── send-daily.yml    # GitHub Actions cron job

```

---

## 🛠️ Setup Instructions

### 1. 🧪 Clone the Repo & Add Your `.env` Secrets

Create a `.env` file locally **(not committed)** and set:

```

TWILIO\_ACCOUNT\_SID=your\_twilio\_sid
TWILIO\_ACCOUNT\_AUTH=your\_twilio\_auth
GROQ\_API\_KEY=your\_groq\_key
TELEGRAM\_BOT=your\_telegram\_bot\_token
WHATSAPP\_NUMBER=your\_phone\_number\_without\_+

````

> On GitHub, store these as **Actions → Repository Secrets**

---

### 2. 📦 Install Requirements

If running locally:

```bash
pip install -r requirements.txt
````

---

### 3. ⚙️ Run Manually (First-Time Test)

* Send `/start` to your Telegram bot (search it on Telegram)
* Trigger GitHub Action manually:

  * Go to **Actions → Send Daily Vocab → Run workflow**

---

### 4. 🕒 GitHub Actions: Scheduled at 9 AM IST

The action is scheduled via this cron:

```yaml
cron: '30 3 * * *'  # 3:30 AM UTC = 9:00 AM IST
```

To change it, edit `.github/workflows/send-daily.yml`

---

## 🧠 How Telegram Opt-In Works

* Users send `/start` → bot adds their `chat_id`
* They get daily messages
* Send `/stop` → bot removes them from the list

---

## 📊 Dataset Used

CSV File: `"Vince's GRE Vocab Compilation and Curation - The Words.csv"`

Column used:

* `Vocab Cartoons App`

---

## 🔐 Security Notes

* Telegram secrets are stored in GitHub secrets
* WhatsApp via Twilio is limited to your number only
* No hosting required — GitHub Actions handles everything

---

## 📩 Example Output

> For the following words explain the meaning and use them in a casual sentence:
> `['mendacious', 'garrulous', 'truculent']`

---

## ✨ Ideas for Future

* Replace `chat_ids.txt` with a Google Sheet or database
* Add button-based opt-in (/subscribe)
* Add word images or examples
* Add Markdown formatting in Telegram

---

## 🧑‍💻 Author

Made with 💡 by \[Your Name]
If this helped you, star ⭐ the repo or fork to customize!

---

```

Let me know if you want to:
- Add a GIF/screenshot to the README
- Automatically update `chat_ids.txt` into Google Sheets
- Add a Telegram message counter leaderboard for fun!
```
