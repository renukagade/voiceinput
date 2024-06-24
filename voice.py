import streamlit as st
import speech_recognition as sr

def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something...")
        audio = r.listen(source)
        
    try:
        text = r.recognize_google(audio)
        st.write("You said:", text)
    except sr.UnknownValueError:
        st.write("Could not understand audio")
    except sr.RequestError as e:
        st.write("Could not request results; {0}".format(e))

def main():
    st.title("Speech to Text Demo")
    st.write("Click below to start recording")
    transcribe_audio()

if __name__ == "__main__":
    main()
