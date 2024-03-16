from dotenv import load_dotenv,find_dotenv
import requests
import os
import io
from PIL import Image
from datetime import datetime
dotenv_path = find_dotenv()
import streamlit as st
load_dotenv(dotenv_path)

# load_dotenv(find_dotenv)
API_TOKEN=os.getenv("API_TOKEN")
def text2img(prompt:str):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}
    payload={
        "inputs":prompt,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes=response.content
    image = Image.open(io.BytesIO(image_bytes))
    timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
    filename=f"{timestamp}.jpg"
    image.save(filename)
    return filename
def main():
    st.title("Text to Image Generation")
    t=st.text_input("Enter your text prompt:")
    if st.button("Generate Image"):
        if t:
            st.write("Generating Image......")
            image_filename = text2img(t)
            st.write("Image generated:")
            st.image(image_filename)
            st.write("Image Path:", image_filename)
if __name__ == "__main__":
    main()