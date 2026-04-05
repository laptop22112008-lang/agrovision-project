import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AgroVision", layout="wide")

# ---------------- SIDEBAR ----------------
st.markdown("""
<style>
.sidebar .sidebar-content {
    background: #0f172a;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌿 AgroVision")

page = st.sidebar.radio("", ["🏠 Dashboard", "📊 Analytics", "📁 History", "ℹ️ About"])

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":

    st.markdown("<h1 style='text-align:center;'>🌿 AgroVision</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:gray;'>Smart Plant Intelligence</h4>", unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns([1,1])

    # -------- UPLOAD CARD --------
    with col1:
        st.markdown("### 📤 Upload Leaf Image")
        uploaded_file = st.file_uploader("Upload image", type=["jpg","png","jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)

    # -------- RESULT CARD --------
    with col2:
        st.markdown("### 📊 Result Overview")

        st.info("Upload image to see analysis")

    st.write("---")

    # -------- STATS CARDS --------
    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric("🌱 Health Score", "85%", "+5%")

    with col4:
        st.metric("⚠️ Risk Level", "Low")

    with col5:
        st.metric("📈 Growth Status", "Stable")

    st.write("---")

    # -------- CHART SECTION --------
    st.markdown("### 📊 Leaf Composition")

    fig, ax = plt.subplots()

    labels = ["Green", "Yellow", "Brown"]
    values = [60, 25, 15]

    ax.pie(values, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    st.markdown("### Overall Performance")

    fig, ax = plt.subplots()

    labels = ["Healthy", "Diseased"]
    values = [70, 30]

    ax.bar(labels, values)
    st.pyplot(fig)

    st.markdown("### Trend Analysis")

    data = np.random.randint(50, 100, 10)
    st.line_chart(data)

# ---------------- HISTORY ----------------
elif page == "📁 History":

    st.title("📁 Analysis History")

    st.info("No records yet")

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":

    st.title("ℹ️ About AgroVision")

    st.markdown("""
    ### 🌿 AgroVision

    AgroVision is an advanced plant analysis system designed to:
    
    - Detect plant health conditions
    - Analyze leaf composition
    - Provide smart insights
    - Track plant history
    
    ### 🚀 Features
    
    - Smart image analysis
    - Clean dashboard UI
    - Real-time insights
    - Analytics visualization
    
    ### 💡 Future Scope
    
    - AI-powered disease detection
    - Weather integration
    - Smart recommendations
    """)
