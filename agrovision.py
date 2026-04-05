import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import rgb_to_hsv
from datetime import datetime

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AgroVision AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# SESSION STATE FIX
# ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ─────────────────────────────────────────
# SAFE PIE FIX (NO CRASH WHEN 100%)
# ─────────────────────────────────────────
def safe_pie_values(values):
    arr = np.array(values, dtype=float)
    total = arr.sum()

    if total <= 0:
        return [34.0, 33.0, 33.0]

    # If one value dominates → clean 100%
    if np.max(arr) / total > 0.99:
        out = [0, 0, 0]
        out[np.argmax(arr)] = 100
        return out

    arr = np.maximum(arr, 0.5)
    arr = arr / arr.sum() * 100
    return arr.tolist()

# ─────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────
def analyze_leaf(image):
    img = np.array(image.convert("RGB")).astype(np.float32)

    rgb_norm = img / 255.0
    hsv = rgb_to_hsv(rgb_norm)

    h = hsv[:, :, 0] * 360
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    candidate = (s > 0.12) & (v > 0.18)

    green = ((h >= 60) & (h <= 160)) & candidate
    yellow = ((h >= 22) & (h < 60)) & candidate
    brown = ((h < 22) | (h > 335)) & candidate

    g = np.sum(green)
    y = np.sum(yellow)
    b = np.sum(brown)

    scores = np.array([g, y, b], dtype=float)
    pie = safe_pie_values(scores)

    total = scores.sum()
    if total == 0:
        gr = yr = br = 1/3
    else:
        gr, yr, br = scores / total

    if gr > 0.6:
        return "GOOD", 99.9, "Healthy Leaf", pie
    elif br > 0.2:
        return "BAD", 85, "Disease Detected", pie
    elif yr > 0.2:
        return "BAD", 80, "Nutrient Deficiency", pie
    else:
        return "BAD", 70, "Mixed Stress", pie

# ─────────────────────────────────────────
# HEADER FIX (NO CUT)
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; font-size:2.2rem; word-break:break-word'>
🌿 AgroVision AI
</h1>
<p style='text-align:center;color:#81c784'>Smart Plant Health Intelligence</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
st.markdown("#### 🔎 Scan a leaf")

uploaded = st.file_uploader(
    "Upload",
    type=["jpg","jpeg","png"],
    key=st.session_state.uploader_key
)

image = None

# ───────── RESET INPUT WHEN NEW IMAGE ─────────
if uploaded:
    if uploaded != st.session_state.last_file:
        st.session_state.last_file = uploaded
        st.session_state.uploader_key += 1
        st.rerun()

    image = Image.open(uploaded)

# ─────────────────────────────────────────
if image:
    result, confidence, condition, pie = analyze_leaf(image)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, use_container_width=True)

    with col2:
        st.success(result)
        st.write(f"Condition: {condition}")
        st.progress(int(confidence))
        st.write(f"{confidence}%")

        c1, c2, c3 = st.columns(3)
        c1.metric("Green", f"{pie[0]:.0f}%")
        c2.metric("Yellow", f"{pie[1]:.0f}%")
        c3.metric("Brown", f"{pie[2]:.0f}%")

    st.write("---")

    # ───────── PIE FIX (NO TEXT OVERLAP) ─────────
    fig, ax = plt.subplots()
    ax.pie(
        pie,
        autopct="%1.1f%%",
        startangle=90,
        labels=None
    )
    ax.legend(["Green","Yellow","Brown"], loc="center left", bbox_to_anchor=(1,0.5))
    st.pyplot(fig)

    st.write("---")

    # ───────── INPUT RESET FIX ─────────
    leaf_name = st.text_input("Leaf name", key=f"name_{st.session_state.uploader_key}")

    if st.button("Save"):
        if leaf_name.strip():
            st.session_state.history.append({
                "name": leaf_name,
                "result": result
            })
            st.success("Saved!")

else:
    st.info("Upload image to start")
