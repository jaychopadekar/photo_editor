import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Import functions from other files
from image_adjustments import adjust_brightness, adjust_contrast, adjust_saturation, sharpen_image, denoise_image
from filters import apply_filter
from utils import validate_file_format

# Initialize session state
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False
    st.session_state.original_image = None
    st.session_state.edited_image = None
    st.session_state.brightness = 0
    st.session_state.contrast = 0
    st.session_state.saturation = 100
    st.session_state.sharpen = False
    st.session_state.resize_width = None
    st.session_state.resize_height = None
    st.session_state.selected_filter = "None"

# Page 1: Image upload
if not st.session_state.image_uploaded:
    st.title("Photo Editing App")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if not validate_file_format(uploaded_file.name):
            st.warning("Only jpg/jpeg/png files are allowed.")
        else:
            st.session_state.original_image = np.array(Image.open(uploaded_file))
            st.session_state.edited_image = np.copy(st.session_state.original_image)
            st.session_state.image_uploaded = True
            st.image(st.session_state.original_image, caption="Uploaded Image", use_column_width=True)

            if st.button("Edit", key="edit_button_upload"):
                st.experimental_rerun()

# Page 2: Image editing
else:
    st.title("Photo Editor")

    # Display original and edited images side-by-side
    st.write("### Image Preview")
    col1, col2 = st.columns(2)

    with col1:
        st.image(st.session_state.original_image, caption="Original Image", use_column_width=True)

    with col2:
        st.image(st.session_state.edited_image, caption="Edited Image", use_column_width=True)

    # Number inputs for adjustments
    if st.session_state.original_image is not None:
        st.session_state.brightness = st.sidebar.number_input("Brightness", -100, 100, st.session_state.brightness)
        st.session_state.contrast = st.sidebar.number_input("Contrast", -100, 100, st.session_state.contrast)
        st.session_state.saturation = st.sidebar.number_input("Saturation", 0, 200, st.session_state.saturation)

        # Add input fields for resizing (width and height)
        st.session_state.resize_width = st.sidebar.number_input(
            "Resize Width", min_value=50, max_value=st.session_state.original_image.shape[1], value=st.session_state.original_image.shape[1]
        )
        st.session_state.resize_height = st.sidebar.number_input(
            "Resize Height", min_value=50, max_value=st.session_state.original_image.shape[0], value=st.session_state.original_image.shape[0]
        )

    # Add a checkbox for sharpening
    st.session_state.sharpen = st.sidebar.checkbox("Apply Sharpening", value=False)

    # Reset Button
    if st.sidebar.button("Reset Adjustments", key="reset_button"):
        st.session_state.brightness = 0
        st.session_state.contrast = 0
        st.session_state.saturation = 100
        st.session_state.resize_width = st.session_state.original_image.shape[1]
        st.session_state.resize_height = st.session_state.original_image.shape[0]
        st.session_state.sharpen = False
        st.session_state.selected_filter = "None"
        st.session_state.edited_image = np.copy(st.session_state.original_image)  # Reset image to original

    # Apply adjustments independently
    adjusted_image = adjust_brightness(st.session_state.original_image, st.session_state.brightness)
    adjusted_image = adjust_contrast(adjusted_image, st.session_state.contrast)
    adjusted_image = adjust_saturation(adjusted_image, st.session_state.saturation)

    # Apply resizing using OpenCV's resize function
    adjusted_image = cv2.resize(adjusted_image, (st.session_state.resize_width, st.session_state.resize_height))

    # Apply sharpening if selected
    if st.session_state.sharpen:
        adjusted_image = sharpen_image(adjusted_image)

    # Denoise Button
    if st.sidebar.button("Denoise Image"):
        adjusted_image = denoise_image(adjusted_image)

    # Filter options
    filter_option = st.sidebar.selectbox("Choose a filter", ["None", "Grayscale", "Sepia", "Negative"], key="filter_select")
    
    # Apply filter
    adjusted_image = apply_filter(adjusted_image, filter_option)

    # Update the edited image in session state
    st.session_state.edited_image = adjusted_image
