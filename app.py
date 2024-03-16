import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from yolo import res
from base64 import b64encode
from dotenv import load_dotenv,find_dotenv
import requests
import os
import io
from datetime import datetime
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
def get_download_link(img_bytes):
    href = f'<a href="data:image/png;base64,{b64encode(img_bytes).decode()}" download="processed_image.png">Click here to download the processed image</a>'
    return href
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
    t = st.text_input("Enter your text prompt:")
    if st.button("Generate Image"):
        if t:
            st.write("Generating Image......")
            image_filename = text2img(t)
            st.write("Image generated:")
            st.image(image_filename)
            image_path = os.path.abspath(image_filename)
            
            # # Load image using the absolute path
            image_array = np.array(Image.open(image_filename))
            annotated_image, dic = res(image_array)
            st.image(annotated_image, caption=dic, use_column_width=True)
            annotated_image_pil = Image.fromarray(annotated_image)
            image_io = BytesIO()
            annotated_image_pil.save(image_io, format="PNG")
            image_data = image_io.getvalue()
            download_link = get_download_link(image_data)
            st.markdown(download_link, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
# Define the get_download_link function



