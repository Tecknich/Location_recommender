import streamlit as st
import requests
from google.cloud import secretmanager

st.title("Location Recommender")
st.markdown("""
    <div style="margin: 10px; padding: 10px; border: 1px solid #EEE; border-radius: 5px; background-color: #f9f9f9;">
        <p style="color: #555;">
            Input a place, location, or a place and location to receive recommendations based on type of establishment 
            and location. Additionally, select any of the results to run the algorithm on that result.
        </p>
    </div>
    """, unsafe_allow_html=True)


def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


project_id = "axiomatic-jet-405520"
secret_id = "GOOGLE_MAPS_API_KEY"
api_key = access_secret_version(project_id, secret_id)


def get_place_id(query, api_key):
    encoded_query = requests.utils.quote(query)
    url = (
        f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={encoded_query}&inputtype=textquery"
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


def reverse_geocode(lat, lng, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
    response = requests.get(url)
    results = response.json().get('results', [])
    if results:
        # Attempting to extract the full address and city
        full_address = results[0].get('formatted_address', 'Unknown Address')
        return full_address
    else:
        return "No results found", "Unknown City"


prompt = st.text_input("Input place and a location")

if 'results' not in st.session_state:
    st.session_state.results = []


def location_recommender(query, api_key):
    if prompt:
        types, location = get_place_id(query, api_key)
        if not types:
            st.write("No results found")
        else:
            new_results = search_similar_places(types, location, api_key)
            st.session_state.results = new_results

            for result in st.session_state.results:
                name = result.get('name')
                loc = result.get('geometry', {}).get('location')
                latitude = loc.get('lat') if loc else None
                longitude = loc.get('lng') if loc else None
                if latitude and longitude:
                    address = reverse_geocode(latitude, longitude, api_key)
                    st.markdown(
                        f"""
                                        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 10px;">
                                            <h4>{name}</h4>
                                            <p><b>Address:</b> {address}</p>
                                        </div>
                                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("Select", key=latitude + longitude):
                        # When the button is clicked, perform an action
                        location_recommender(address, api_key)

                else:
                    st.write(f"Name: {name}")


location_recommender(prompt, api_key)
