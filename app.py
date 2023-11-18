import streamlit as st
import requests
from transformers import pipeline

model = pipeline(task="automatic-speech-recognition", model="openai/whisper-large-v3")
api_key = 'AIzaSyDGPL1I31RJeAnaDnPoTpbfjNjbp7kvYO0'


def get_place_id(query, api_key):
    url = (f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery"
           f"&fields=types, geometry&key={api_key}")

    response = requests.get(url)
    results = response.json().get('candidates', [])
    if results:
        location = results[0].get('geometry', {}).get('location', {})
        types = results[0].get('types', [])
        return types, location
    else:
        return None, None


def search_similar_places(types, location, api_key, radius=5000):
    # Join types to form a string for the API query
    types_query = "|".join(types)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={types_query}&key={api_key}"
    response = requests.get(url)
    results = response.json().get('results', [])
    return results


st.title("Location Recommender")

prompt = st.chat_input("Input place and a location")
types, location = get_place_id(prompt, api_key)
if types is None:
    st.write("No results found")
else:
    results = search_similar_places(types, location, api_key)
    st.write(results)
