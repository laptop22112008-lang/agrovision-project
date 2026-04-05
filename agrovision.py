import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AgroVision", layout="wide")

# ---------------- NAVIGATION (TOP) ----------------
page = st.radio(
    "",
    ["🏠 Dashboard", "📊 Analytics", "📁 History", "ℹ️ About"],
    horizontal=True
)

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- MODEL (STABLE LOGIC) ----------------
def analyze_leaf(image):
    img = np.array(image)

    r = np.mean(img[:, :, 0])
    g = np.mean(img[:, :, 1])
    b = np.mean(img[:, :, 2])

    total = r + g + b + 1

    green_ratio = g / total
    red_ratio = r / total

    # Balanced decision (not too strict)
    if green_ratio > 0.38:
        result = "GOOD"
        condition = "Healthy Leaf"
        confidence = round(green_ratio * 100, 2)
    elif red_ratio > 0.34:
        result = "BAD"
        condition = "Disease Detected"
        confidence = round(red_ratio * 100, 2)
    else:
        result = "BAD"
        condition = "Nutrient Deficiency"
        confidence = round((red_ratio + (1-green_ratio)) * 50, 2)

    return result, confidence, condition, [g, r, b]

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":

    st.markdown("<h1 style='text-align:center;'>🌿 AgroVision</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:gray;'>Smart Plant Intelligence</h4>", unsafe_allow_html=True)

    st.write("")

    uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "png", "jpeg"])

    # ❗ ONLY SHOW RESULT AFTER UPLOAD
    if uploaded_file:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns([1,1])

        with col1:
            st.image(image, use_column_width=True)

        with col2:
            result, confidence, condition, values = analyze_leaf(image)

            # -------- RESULT BOX --------
            if result == "GOOD":
                st.success(f"Result: {result}")
            else:
                st.error(f"Result: {result}")

            st.write(f"Confidence: {confidence}%")
            st.write(f"Condition: {condition}")

        st.write("---")

        # -------- PIE CHART --------
        st.markdown("### 📊 Leaf Composition")

        fig, ax = plt.subplots()
        labels = ["Green", "Red", "Blue"]
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

        # -------- SAVE --------
        name = st.text_input("Enter Leaf Name")

        if st.button("💾 Save to History"):
            st.session_state.history.append({
                "name": name,
                "result": result,
                "confidence": confidence,
                "condition": condition
            })
            st.success("Saved!")

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":

    st.title("📊 Analytics")

    if st.session_state.history:
        good = sum(1 for i in st.session_state.history if i["result"] == "GOOD")
        bad = sum(1 for i in st.session_state.history if i["result"] == "BAD")

        fig, ax = plt.subplots()
        ax.pie([good, bad], labels=["GOOD", "BAD"], autopct='%1.1f%%')
        st.pyplot(fig)
    else:
        st.info("No data yet")

# ---------------- HISTORY ----------------
elif page == "📁 History":

    st.title("📁 History")

    if st.session_state.history:
        for item in st.session_state.history:
            st.write("---")
            st.write(f"Name: {item['name']}")
            st.write(f"Result: {item['result']}")
            st.write(f"Confidence: {item['confidence']}%")
            st.write(f"Condition: {item['condition']}")
    else:
        st.info("No history yet")

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":

    st.title("ℹ️ About AgroVision")

    st.markdown("""
    ### 🌿 AgroVision

    - Smart plant health detection system  
    - Uses image-based analysis  
    - Provides real-time results  
    - Tracks history and analytics  

    ### 🚀 Features

    - Leaf health detection  
    - Analytics dashboard  
    - Clean UI  
    - Fast processing  

    ### 🔮 Future Scope

    - AI model (CNN)  
    - Disease classification  
    - Weather integration  
    """)
