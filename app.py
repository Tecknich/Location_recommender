import streamlit as st
from transformers import pipeline
from PIL import Image

model = pipeline(task="image-classification", model="sallyanndelucia/resnet_weather_model")


def predict(image):
    predictions = model(image)
    return {p["label"]: p["score"] for p in predictions}

def load_image(image):
    img = Image.open(image)
    return img

st.title("Test")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = load_image(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")

    if st.button('Predict'):
        prediction = predict(image)

        for i in range(2):
            st.write(prediction)
