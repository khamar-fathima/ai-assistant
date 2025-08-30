# app.py
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile

# -----------------------
# Load API Key
# -----------------------
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    st.error("⚠️ Gemini API key not found in .env!")
else:
    genai.configure(api_key=gemini_key)

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🎤 Gemini AI Assistant with Voice")

if "history" not in st.session_state:
    st.session_state.history = "You are a helpful AI assistant.\n"

# Show chat history
st.subheader("Chat")
for line in st.session_state.history.split("\n"):
    if line.startswith("User:"):
        st.markdown(f"**🧑 You:** {line[6:]}")
    elif line.startswith("Assistant:"):
        st.markdown(f"**🤖 AI:** {line[11:]}")

# -----------------------
# Text Input
# -----------------------
user_input = st.text_input("💬 Type your message:")

# -----------------------
# Voice Input (enabled)
# -----------------------
st.write("🎙️ Or ask by voice:")
voice = mic_recorder(start_prompt="🎤 Record", stop_prompt="🛑 Stop", just_once=True)

if voice:
    user_input = voice["text"] if "text" in voice else None

# -----------------------
# Send Message
# -----------------------
if st.button("Send") and user_input:
    st.session_state.history += f"User: {user_input}\n"
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(st.session_state.history)
        answer = response.text.strip()
    except Exception as e:
        answer = f"⚠️ Gemini API error: {str(e)}"
    st.session_state.history += f"Assistant: {answer}\n"
    # Text-to-speech playback of the AI's answer
    try:
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")
    except Exception as tts_error:
        st.warning(f"⚠️ Could not generate speech: {tts_error}")
    st.rerun()