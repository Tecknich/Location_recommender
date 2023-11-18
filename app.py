import streamlit as st
import requests
from transformers import pipeline

model = pipeline(task="automatic-speech-recognition", model="openai/whisper-large-v3")
api_key = 'AIzaSyDGPL1I31RJeAnaDnPoTpbfjNjbp7kvYO0'

def get_place_id(query, api_key):
    url = (f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery"
           f"&fields=types&key={api_key}")

    response = requests.get(url)
    results = response.json().get('candidates', [])
    if results:
        return results[0].get('types', [])
    else:
        return "No results found"

st.title("Location Recommender")

prompt = st.chat_input("Input place")

type = get_place_id(prompt, api_key)
st.write(type)

