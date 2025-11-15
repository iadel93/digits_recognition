import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import requests

SERVER_URL = "http://localhost:8000"

def predict_digit(image_data: list) -> dict:
    """Predict the digit from the image data using the server."""
    # Convert the image data to a list
    image_list = image_data.flatten().tolist()
    payload = {"image_data": image_list}
    response = requests.post(f"{SERVER_URL}/predict/", json=payload)
    return response.json()


st.set_page_config(page_title="Digits Recognition App")
st.header("Digits Recognition App")
st.subheader("Draw a Digit (28×28)")

# Set up the canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=30,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas_app",
)

# Display controls
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Save Drawing", use_container_width=True):
        if canvas_result.image_data is not None:
            # Convert canvas to PIL Image
            img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype('uint8'))
            
            # Convert to grayscale
            img_gray = img.convert('L')
            
            # Resize to 28x28
            img_28 = img_gray.resize((28, 28), Image.Resampling.LANCZOS)
            
            # Save the image
            img_28.save("digit.png")
            
            st.success("✓ Drawing saved as digit.png")
            st.image(img_28, caption="28x28 Digit", width=150)
        else:
            st.error("Please draw something first")

with col2:
    if st.button("Clear Canvas", use_container_width=True):
        st.rerun()

with col3:
    pass

# File uploader as alternative
st.divider()
st.subheader("Or Upload a Digit Image")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('L')
    img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    st.subheader("28x28 Preview")
    st.image(img_resized, caption="Your Digit (28x28)", width=150)
    
    if st.button("Save Uploaded Image", key="save_upload_btn"):
        img_resized.save("digit.png")
        st.success("✓ Image saved as digit.png")

# Prediction
st.divider()
st.subheader("Predict the Digit")
predict_button = st.button("Predict Digit")
if predict_button:
    if canvas_result.image_data is not None:
        # Process canvas image
        img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype('uint8'))
        img_gray = img.convert('L')
        img_28 = img_gray.resize((28, 28))
        img_array = np.array(img_28).reshape(28, 28)
        normalized_img = 255 - img_array  # Invert colors if necessary
        
        prediction = predict_digit(normalized_img)
        st.image(normalized_img, caption="28x28 Digit", width=150)
        st.success(f"Predicted Digit: {prediction['prediction']}")
    elif uploaded_file is not None:
        # Process uploaded image
        img_array = np.array(img_resized).reshape(28, 28)
        
        prediction = predict_digit(img_array)
        st.success(f"Predicted Digit: {prediction['prediction']}")
    else:
        st.error("Please draw or upload an image first")