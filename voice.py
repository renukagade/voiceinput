import streamlit as st
import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

BASE_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

# Function to fetch word data from API
# (Rest of the functions remain unchanged as per your previous code)

def speak_text(text):
    tts = gTTS(text=text, lang='en')  # Adjust 'lang' parameter as needed for other languages
    tts.save("output.mp3")
    os.system("start output.mp3")  # Opens the mp3 file with the default application

# Streamlit UI
st.title("Enhanced Multilingual Dictionary Bot")
st.write("Enter a word or use voice input to get its meaning.")

word = st.text_input("Enter a word:")

# Streamlit interface
        
if word:
    word_data = get_word_data(word)
    if word_data:
        meaning = get_word_meaning(word_data)
        part_of_speech = get_part_of_speech(word_data)
        examples = get_example_sentences(word_data)
        synonyms, antonyms = get_synonyms_antonyms(word)

        st.write(f"Word: {word}")
        st.write(f"Part of Speech: {part_of_speech}")
        st.write(f"Meaning: {meaning}")

        if examples:
            st.write("Examples:")
            for example in examples:
                st.write(f"- {example}")

        if synonyms:
            st.write("Synonyms:")
            st.write(", ".join(synonyms))

        if antonyms:
            st.write("Antonyms:")
            st.write(", ".join(antonyms))

        dest_lang = st.selectbox("Translate to language:", ["es", "fr", "de", "zh-cn", "hi"])
        translated_meaning = translate_text(meaning, dest_lang)
        st.write(f"Translated Meaning: {translated_meaning}")
        
        if st.button("Speak Meaning"):
            speak_text(meaning)

        if st.button("Speak Translated Meaning"):
            speak_text(translated_meaning)

    else:
        st.write("No data found for the given word.")
