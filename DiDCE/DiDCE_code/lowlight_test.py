import streamlit as st
import torch
import torchvision.transforms as T
import torchvision.utils as vutils
from PIL import Image
import numpy as np
import os
import model  # Make sure model.py from Zero-DiDCE is in the same folder or in PYTHONPATH

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
@st.cache_resource
def load_model():
    net = model.enhance_net_nopool().to(device)
    net.load_state_dict(torch.load("snapshots/Epoch99.pth", map_location=device))
    net.eval()
    return net

def enhance_image(input_img: Image.Image, net):
    img = np.asarray(input_img).astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.no_grad():
        enhanced, _ = net(img_tensor)

    enhanced = enhanced.squeeze(0).cpu()
    return enhanced

# Custom CSS for colorful interactive UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fceabb, #f8b500);
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 3em;
        font-weight: bold;
        color: #3b3b98;
        text-align: center;
        margin-top: 20px;
    }
    .subtitle {
        font-size: 1.3em;
        color: #1e272e;
        text-align: center;
        margin-bottom: 20px;
    }
    .upload-box {
        border: 2px dashed #3b3b98;
        padding: 20px;
        border-radius: 10px;
        background-color: #fffbea;
    }
    .result-section {
        border-radius: 10px;
        background-color: #ffffffcc;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.set_page_config(page_title="Zero-DiDCE Enhancer", layout="centered")
st.markdown('<div class="title">🌈 Low-Light Enhancer with Zero-DiDCE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a photo, let the magic happen ✨</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload a low-light image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGB")
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.image(input_image, caption="🕯️ Original Image", use_column_width=True)

    model_net = load_model()
    enhanced_output = enhance_image(input_image, model_net)

    st.subheader("📸 Enhanced Image")
    st.image(vutils.make_grid(enhanced_output, normalize=True).permute(1, 2, 0).numpy(), use_column_width=True)

    # Download button
    result_image = T.ToPILImage()(enhanced_output)
    st.download_button("💾 Download Enhanced Image", data=result_image.tobytes(), file_name="enhanced.png", mime="image/png")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="upload-box">📁 Drag and drop or browse an image file above to enhance your low-light image.</div>', unsafe_allow_html=True)
