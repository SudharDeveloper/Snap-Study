# 📚 Snap & Study

> **Snap your notes. Master the concepts. Text yourself the revision guide.**

Snap & Study is an intelligent AI study companion powered by Google Gemini and Twilio. Students can upload photos of handwritten notes, textbook pages, math/physics problems, or code snippets, receive instant step-by-step explanations, and text themselves structured study cheat sheets directly to WhatsApp!

---

## ✨ Features

- 📸 **Multimodal Study Assistant**: Snap photos of handwritten notes, diagrams, math problems, or textbook excerpts.
- 💡 **Step-by-Step Problem Solving**: Detailed conceptual breakdowns, formulas, definitions, and memory aids.
- 📲 **WhatsApp Revision Cheat Sheets**: Send formatted high-yield study summaries and exam cheat sheets straight to your WhatsApp via Twilio.
- 🎨 **Interactive Streamlit UI**: Chat interface with markdown math rendering and session management.

---

## 🛠️ Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **AI / LLM**: [Google GenAI SDK](https://github.com/google/generative-ai-python) (`gemini-2.5-flash`)
- **Messaging**: [Twilio Python SDK](https://www.twilio.com/) (WhatsApp API)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SudharDeveloper/Snap-Study.git
cd Snap-Study
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets
Create `.streamlit/secrets.toml` in the project root:
```toml
GEMINI_API_KEY = "your-gemini-api-key"

TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
TWILIO_CONTENT_SID = "your-content-sid-or-blank"
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📜 License
MIT License. Feel free to use and customize for your own learning!
