import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment


# Load the CSS file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define the HTML for the banner
banner_html = """
<div class="full-width-banner">
    <img src="https://zeroheight.com/uploads/DAKqHhnDoTprAFJDxyKYEg.jpg">
    <h2>Data Examiner</h2>
</div>
"""

# Embed the HTML in Streamlit
st.markdown(banner_html, unsafe_allow_html=True)

# Add some space below the banner
st.write("<br>", unsafe_allow_html=True)

# Get user input
audio_value = st.audio_input("Record a your input")

if audio_value:
    st.audio(audio_value)
    audio_bytes = audio_value.read()
    
    # Save the audio file
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)
    
    # Convert audio to text
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav("audio.wav")
    audio.export("audio_converted.wav", format="wav")
    
    with sr.AudioFile("audio_converted.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        st.write("Input:", text)

    
