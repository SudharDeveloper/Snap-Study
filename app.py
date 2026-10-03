import json
 
import streamlit as st
from google import genai
from google.genai import types
from twilio.rest import Client as TwilioClient
 
from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE
 
MODEL_NAME = "gemini-2.5-flash"
APP_VERSION = "snap_and_study_v2"
 
st.set_page_config(page_title="Snap & Study", page_icon="📚", layout="centered")
 
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
TWILIO_CONTENT_SID = st.secrets.get("TWILIO_CONTENT_SID", "")
 
 
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)
 
 
@st.cache_resource
def get_twilio_client():
    return TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
 
 
gemini_client = get_gemini_client()
twilio_client = get_twilio_client()
 
 
def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.markdown(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])
 
 
def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])
 
 
def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"
 
 
def clean_whatsapp_text(text):
    if not text:
        return "No study summary available."
    text = " ".join(text.split())  # collapse excessive whitespace/newlines
    return text[:1500] + "..." if len(text) > 1500 else text
 
 
def send_whatsapp(to_number, user_name, summary):
    try:
        # Normalize and clean phone number
        cleaned_num = str(to_number).strip().replace(" ", "").replace("-", "")
        if cleaned_num.startswith("whatsapp:"):
            cleaned_num = cleaned_num.replace("whatsapp:", "")
        if not cleaned_num.startswith("+"):
            cleaned_num = f"+{cleaned_num}"
        
        target = f"whatsapp:{cleaned_num}"
        
        # Try sending using Content Template if valid SID provided
        if TWILIO_CONTENT_SID and TWILIO_CONTENT_SID.startswith("HX"):
            try:
                content_variables = json.dumps(
                    {"1": user_name, "2": clean_whatsapp_text(summary)}, ensure_ascii=False
                )
                message = twilio_client.messages.create(
                    from_=TWILIO_WHATSAPP_FROM,
                    to=target,
                    content_sid=TWILIO_CONTENT_SID,
                    content_variables=content_variables,
                )
                return True, message.sid
            except Exception:
                # If Content Template fails, fallback to direct text body
                pass

        # Fallback to direct text body (works seamlessly with Sandbox)
        message_body = f"Hi {user_name}! 📚 Here is your Snap & Study revision cheat sheet:\n\n{summary}"
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=target,
            body=message_body,
        )
        return True, message.sid
    except Exception as error:
        return False, str(error)
 
 
# Automatically wipe any old MacroSnap memory from active browser sessions
if st.session_state.get("app_version") != APP_VERSION:
    if "onboarded" in st.session_state:
        st.session_state.chat = gemini_client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        st.session_state.messages = []
    st.session_state.app_version = APP_VERSION
 
 
# Step 1: Student Onboarding
if "onboarded" not in st.session_state:
    st.title("📚 Snap & Study")
    st.caption("Snap your notes. Master the concepts. Text yourself the revision guide.")
    
    with st.form("onboarding_form"):
        name = st.text_input("Your Name", placeholder="e.g. Alex")
        whatsapp_number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
            help="This is the number Snap & Study will text your study cheat sheet to.",
        )
        submitted = st.form_submit_button("Start Studying 🚀", use_container_width=True)
        
    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("Please enter your name and WhatsApp number.")
        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = whatsapp_number.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.session_state.app_version = APP_VERSION
            st.rerun()
    st.stop()
 
# Sidebar Controls
with st.sidebar:
    st.title("📚 Snap & Study")
    st.write(f"👤 **Student:** {st.session_state.name}")
    st.write(f"📲 **WhatsApp:** `{st.session_state.whatsapp_number}`")
    st.divider()
    
    st.subheader("💡 What you can snap:")
    st.markdown("""
    - 📐 **Math & Physics problems**
    - 📝 **Handwritten study notes**
    - 📖 **Textbook pages & diagrams**
    - 💻 **Code snippets & bugs**
    - 🧪 **Chemistry structures & equations**
    """)
    st.divider()
    
    if st.button("🔄 Start New Study Session", use_container_width=True):
        st.session_state.chat = gemini_client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        st.session_state.messages = []
        st.rerun()

# Step 2: Study Interface
header_col, button_col = st.columns([5, 3], vertical_alignment="center")
 
with header_col:
    st.title("📚 Snap & Study")
 
with button_col:
    send_disabled = len(st.session_state.messages) == 0
    if st.button("📤 Send Notes to WhatsApp", disabled=send_disabled, use_container_width=True):
        with st.spinner("Generating your revision cheat sheet..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your WhatsApp 📲")
        else:
            st.error(f"Couldn't send that: {info}")
 
st.caption(f"Studying as **{st.session_state.name}** • Summary destination: **{st.session_state.whatsapp_number}**")
 
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)
 
user_input = st.chat_input(
    "Ask a study question, or attach a photo of your notes / textbook / problem",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)
 
if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []
 
    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("Please analyze this study material in detail. Explain the core concepts, solve any questions step-by-step, and list key takeaways and formulas.")
 
    with st.spinner("Analyzing study material..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)
