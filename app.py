import streamlit as st
import requests
from transformers import pipeline

model = pipeline("text2text-generation", model="RUCAIBox/mtl-data-to-text")
api_key = 'AIzaSyDGPL1I31RJeAnaDnPoTpbfjNjbp7kvYO0'


def get_place_id(query, api_key):
    encoded_query = requests.utils.quote(query)
    url = (f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={encoded_query}&inputtype=textquery"
           f"&fields=types,geometry&key={api_key}")

    response = requests.get(url)
    results = response.json().get('candidates', [])
    if results:
        location = results[0].get('geometry', {}).get('location', {})
        types = results[0].get('types', [])
        return types, location
    else:
        return None, None

def search_similar_places(types, location, api_key, radius=5000):
    location_str = f"{location['lat']},{location['lng']}" if location else ""
    types_query = "|".join(types)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_str}&radius={radius}&type={types_query}&key={api_key}"
    response = requests.get(url)
    results = response.json().get('results', [])
    return results

st.title("Location Recommender")

prompt = st.text_input("Input place and a location")

if prompt:
    types, location = get_place_id(prompt, api_key)
    if not types:
        st.write("No results found")
    else:
        results = search_similar_places(types, location, api_key)
        place_names = [result['name'] for result in results if 'name' in result]
        st.write(place_names)
