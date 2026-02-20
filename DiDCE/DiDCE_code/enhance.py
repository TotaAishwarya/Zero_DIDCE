# 📁 FILE: enhance.py

import streamlit as st
from PIL import Image, ImageEnhance
import torch
import torchvision.transforms as T
import torchvision.utils as vutils
import numpy as np
from io import BytesIO
import model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def load_model():
    net = model.enhance_net_nopool().to(device)
    net.load_state_dict(torch.load("snapshots/Epoch99.pth", map_location=device))
    net.eval()
    return net

def preprocess_webcam_image(img: Image.Image):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)
    return img.resize((400, 400))

def enhance_image(input_img: Image.Image, net):
    img = np.asarray(input_img).astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(device)
    with torch.no_grad():
        enhanced, _ = net(img_tensor)
    return enhanced.squeeze(0).cpu()

def run():
    if not st.session_state.get("logged_in", False):
        st.warning("🔐 Please login to access this page.")
        st.stop()  # ⛔ Stop execution of the rest of the page

    st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .title-enhance { font-size: 2.2em; text-align: center; font-weight: 700; color: #5c5470; margin-bottom: 0.5rem; }
    .subtitle-enhance { font-size: 1.2em; text-align: center; color: #7a6e94; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title-enhance">✨ Enhance Your Image</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-enhance">Choose an image and apply enhancement using Zero-DiDCE</div>', unsafe_allow_html=True)

    col_input = st.columns(1)[0]
    with col_input:
        source = st.radio("📷 Choose Image Source", ["📁 Upload Image", "📸 Use Webcam"])

    input_image = None
    if source == "📁 Upload Image":
        file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
        if file:
            input_image = Image.open(file).convert("RGB")
    elif source == "📸 Use Webcam":
        cam = st.camera_input("Capture image from webcam")
        if cam:
            webcam_img = Image.open(cam).convert("RGB")
            input_image = preprocess_webcam_image(webcam_img)

    if input_image:
        st.markdown("### 🔍 Result Preview")
        model_net = load_model()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🕯️ Original Image")
            st.image(input_image, use_column_width=True)

        with col2:
            with st.spinner("⚙️ Enhancing using Zero-DiDCE..."):
                enhanced_output = enhance_image(input_image, model_net)
                result_image = T.ToPILImage()(enhanced_output)
                enhanced_np = vutils.make_grid(enhanced_output, normalize=True).permute(1, 2, 0).numpy()

            st.markdown("#### ✨ Enhanced Image")
            st.image(enhanced_np, use_column_width=True)

            buffer = BytesIO()
            result_image.save(buffer, format="PNG")
            byte_data = buffer.getvalue()

            st.download_button("💾 Download Enhanced Image", data=byte_data, file_name="enhanced_output.png", mime="image/png")
