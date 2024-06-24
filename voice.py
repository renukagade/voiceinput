import streamlit as st
from streamlit_webrtc import webrtc_streamer, ClientSettings, WebRtcMode
import av
import speech_recognition as sr
import numpy as np

# Initialize session state for webrtc
if "webrtc_initialized" not in st.session_state:
    st.session_state["webrtc_initialized"] = False
    st.session_state["transcription"] = ""

# Function to process audio frames
def audio_processor_factory():
    recognizer = sr.Recognizer()

    def process_audio(frame: av.AudioFrame):
        audio = frame.to_ndarray()
        audio = audio.mean(axis=1)  # Convert stereo to mono
        sample_rate = frame.sample_rate

        # Convert numpy array to AudioData
        audio_data = sr.AudioData(audio.tobytes(), sample_rate, frame.format.bits_per_sample // 8)

        try:
            text = recognizer.recognize_google(audio_data)
            st.session_state["transcription"] = text
        except sr.UnknownValueError:
            st.session_state["transcription"] = "Could not understand audio"
        except sr.RequestError as e:
            st.session_state["transcription"] = f"Could not request results from Google Speech Recognition service; {e}"

    return process_audio

# Streamlit interface
if st.button("Use Voice Input") and not st.session_state["webrtc_initialized"]:
    st.session_state["webrtc_initialized"] = True
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDRECV,
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": False, "audio": True},
        ),
        audio_processor_factory=audio_processor_factory,
    )

    if webrtc_ctx.state.playing:
        st.write("Listening...")
        if st.session_state["transcription"]:
            st.write("You said: ", st.session_state["transcription"])

# Display the transcription if available
if st.session_state["webrtc_initialized"] and st.session_state["transcription"]:
    st.write("You said: ", st.session_state["transcription"])
