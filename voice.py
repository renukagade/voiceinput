import streamlit as st
import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

BASE_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

def get_word_data(word):
    url = f"{BASE_URL}{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
        else:
            return None
    else:
        return None

def get_word_meaning(data):
    if 'meanings' in data:
        definitions = data['meanings'][0]['definitions']
        if definitions:
            return definitions[0]['definition']
    return "No definition found."

def get_part_of_speech(data):
    if 'meanings' in data:
        return data['meanings'][0]['partOfSpeech']
    return "Unknown"

def get_example_sentences(data):
    examples = []
    if 'meanings' in data:
        definitions = data['meanings'][0]['definitions']
        if definitions:
            for definition in definitions:
                if 'example' in definition:
                    examples.append(definition['example'])
    return examples

def get_synonyms_antonyms(data):
    synonyms = []
    antonyms = []
    if 'meanings' in data:
        definitions = data['meanings'][0]['definitions']
        if definitions:
            for definition in definitions:
                if 'synonyms' in definition:
                    synonyms.extend(definition['synonyms'])
                if 'antonyms' in definition:
                    antonyms.extend(definition['antonyms'])
    return synonyms, antonyms

def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

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
        synonyms, antonyms = get_synonyms_antonyms(word_data)

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

        dest_lang = st
