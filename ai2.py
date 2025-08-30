# ai2.py
import os
import logging
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai

# -----------------------
# SUPPRESS NOISE
# -----------------------
logging.getLogger('speech_recognition').setLevel(logging.CRITICAL)

# -----------------------
# LOAD ENV VARIABLES
# -----------------------
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("Gemini API key not found in .env!")
genai.configure(api_key=gemini_key)

# -----------------------
# SPEAK FUNCTION
# -----------------------
def speak(text):
    os.system(f'say "{text}"')

# -----------------------
# LISTEN FUNCTION
# -----------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1.0)  # better noise filtering
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        if len(command.strip()) < 2:  # ignore very short/noisy inputs
            return ""
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Could not request results; check your internet.")
        return ""

# -----------------------
# MAIN LOOP
# -----------------------
conversation_history = "You are a helpful AI assistant.\n"

speak("Hello! I am your AI Assistant. Just ask me anything, or say 'exit' to quit.")
print("🤖 AI Assistant ready! Ask me anything.")

while True:
    user_input = listen()
    
    if user_input in ["stop", "terminate"]:
        speak("Stopping as you requested. Goodbye!")
        print("Stopping as you requested. Goodbye!")
        break
    
    if user_input in ["exit", "quit"]:
        speak("Goodbye!")
        print("Goodbye!")
        break
    
    if user_input.strip() == "":
        continue
    
    conversation_history += f"User: {user_input}\n"
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(conversation_history)
        answer = response.text.strip()
    except Exception as e:
        answer = f"⚠️ Gemini API error: {str(e)}"
    conversation_history += f"Assistant: {answer}\n"
    print("AI Assistant:", answer)
    speak(answer)