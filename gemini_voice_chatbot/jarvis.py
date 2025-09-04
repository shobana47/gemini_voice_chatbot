import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import tempfile
import os

# 🔑 Configure Gemini API Key
genai.configure(api_key="AIzaSyBuDVhbq7dgY68-eFTDXBpRqgI7EO_PLhc")   # replace with your actual key

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()
model = genai.GenerativeModel("gemini-1.5-flash")

def listen_and_convert():
    """Listen from microphone and convert speech to text."""
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="en-IN")
            st.write(f"👉 You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
            return None
        except sr.RequestError:
            st.error("⚠️ Speech Recognition API unavailable.")
            return None

def ask_gemini(prompt):
    """Send user input to Gemini and get response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini error: {e}"

def speak(text):
    """Convert text to speech and return audio file path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
    tts.save_to_file(text, filename)
    tts.runAndWait()
    return filename

# Streamlit UI
st.title("🎙️ Gemini Voice Chatbot")
st.write("Talk to Gemini with voice or text. Say **exit/quit/stop** to end.")

if st.button("🎤 Speak"):
    user_input = listen_and_convert()
    if user_input:
        if user_input.lower() in ["exit", "quit", "stop"]:
            st.success("👋 Chatbot ended.")
        else:
            reply = ask_gemini(user_input)
            st.write(f"🤖 Gemini: {reply}")

            audio_file = speak(reply)
            st.audio(audio_file, format="audio/mp3")

# Text input as fallback
user_text = st.text_input("💬 Or type your question here:")
if st.button("Send"):
    if user_text:
        reply = ask_gemini(user_text)
        st.write(f"🤖 Gemini: {reply}")

        audio_file = speak(reply)
        st.audio(audio_file, format="audio/mp3")
        
# cd "C:\Users\SHOBANA G\Desktop\Project\gemini_voice_chatbot"
# # python -m streamlit run jarvis.py