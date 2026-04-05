# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import rgb_to_hsv
from datetime import datetime
import io
import hashlib
import time

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

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
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: linear-gradient(180deg, #071018 0%, #0c1722 100%);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

h1, h2, h3, h4, h5 {
    font-family: 'Sora', sans-serif;
    color: #eef6ff;
}

p, li, label, .stMarkdown, .stText, .stCaption {
    color: #d5e3f0;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08111a 0%, #0c1622 100%);
    border-right: 1px solid #183248;
}
section[data-testid="stSidebar"] * {
    color: #eef6ff;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #14b8a6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.55rem 1.2rem !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 18px rgba(14,165,233,0.16);
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(20,184,166,0.28);
}

.stTextInput > div > div > input {
    background: #0b1723 !important;
    color: #edf7ee !important;
    border: 1px solid #23405c !important;
    border-radius: 12px !important;
    padding: 0.7rem 0.9rem !important;
}
.stFileUploader {
    background: #0b1723;
    border: 1.5px dashed #23405c;
    border-radius: 14px;
    padding: 0.8rem;
}

.hero-card, .main-card, .stat-card, .analysis-card, .history-card, .about-card {
    background: linear-gradient(180deg, rgba(10,22,34,0.95), rgba(8,17,26,0.98));
    border: 1px solid #1f3950;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.22);
}

.hero-card {
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}

.main-card {
    padding: 1.2rem 1.3rem;
    margin-bottom: 1rem;
}

.stat-card {
    padding: 1rem;
    text-align: center;
}

.analysis-card {
    padding: 1rem 1.1rem;
    margin-top: 0.85rem;
}

.history-card {
    padding: 1rem 1.1rem;
    margin-bottom: 0.9rem;
}

.about-card {
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}

.good-badge {
    display: inline-block;
    padding: 0.45rem 0.95rem;
    border-radius: 999px;
    background: rgba(20, 184, 166, 0.15);
    border: 1px solid #14b8a6;
    color: #99f6e4;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.bad-badge {
    display: inline-block;
    padding: 0.45rem 0.95rem;
    border-radius: 999px;
    background: rgba(248, 113, 113, 0.12);
    border: 1px solid #fb7185;
    color: #fecdd3;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.sev-low {
    display: inline-block;
    background: #123c36;
    border: 1.5px solid #14b8a6;
    color: #99f6e4;
    border-radius: 20px;
    padding: 4px 16px;
    font-weight: 600;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
}
.sev-medium {
    display: inline-block;
    background: #3a2c10;
    border: 1.5px solid #f59e0b;
    color: #fde68a;
    border-radius: 20px;
    padding: 4px 16px;
    font-weight: 600;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
}
.sev-high {
    display: inline-block;
    background: #40151a;
    border: 1.5px solid #fb7185;
    color: #fecdd3;
    border-radius: 20px;
    padding: 4px 16px;
    font-weight: 600;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
}

.soft-label {
    color: #8fb1cc;
    font-size: 0.88rem;
}
.soft-value {
    color: #f1f7ff;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
}
.small-note {
    color: #87a5bf;
    font-size: 0.82rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "saved_hashes" not in st.session_state:
    st.session_state.saved_hashes = []

if "save_nonce" not in st.session_state:
    st.session_state.save_nonce = 0

# ─────────────────────────────────────────
# TREATMENT DATABASE
# ─────────────────────────────────────────
TREATMENTS = {
    "Healthy Leaf": {
        "card_class": "",
        "icon": "✅",
        "title": "Plant is healthy — maintain current care",
        "tips": [
            "Continue the regular watering schedule",
            "Apply balanced NPK fertiliser monthly",
            "Monitor for early signs of pests or discolouration",
            "Ensure adequate sunlight and airflow between plants",
        ],
    },
    "Mostly Healthy": {
        "card_class": "",
        "icon": "🟢",
        "title": "Mostly healthy — only minor stress detected",
        "tips": [
            "Inspect the plant again in 3–5 days",
            "Check if the leaf is getting too much direct sun",
            "Avoid overwatering and keep soil moisture stable",
            "Remove only clearly damaged parts if needed",
        ],
    },
    "Disease Detected": {
        "card_class": "danger",
        "icon": "🦠",
        "title": "Disease treatment recommended",
        "tips": [
            "Remove and dispose of heavily infected leaves immediately",
            "Apply a copper-based or neem oil fungicide/bactericide spray",
            "Avoid overhead watering — water at the base only",
            "Increase plant spacing to improve air circulation",
            "Re-inspect after 7 days and repeat treatment if needed",
        ],
    },
    "Nutrient Deficiency": {
        "card_class": "warn",
        "icon": "🌱",
        "title": "Nutrient correction needed",
        "tips": [
            "Test soil pH — ideal range is 6.0–7.0 for most crops",
            "Apply a micronutrient-rich foliar spray (Fe, Mg, Zn)",
            "Add organic compost to improve soil structure and retention",
            "Consider a slow-release fertiliser with balanced N-P-K",
            "Avoid over-watering which leaches nutrients from the soil",
        ],
    },
    "Mixed Stress": {
        "card_class": "warn",
        "icon": "⚠️",
        "title": "Mixed stress detected — monitor carefully",
        "tips": [
            "Check watering consistency first",
            "Inspect for pests, fungal spots, and leaf curling",
            "Reduce heat stress with partial shade if needed",
            "Re-scan the leaf under natural light for confirmation",
            "If symptoms spread, isolate the plant from others",
        ],
    },
}

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def image_to_bytes(img: Image.Image):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    return buf.getvalue()


def is_leaf(image: Image.Image) -> bool:
    img = np.array(image.convert("RGB")).astype(np.float32)
    rgb_norm = img / 255.0
    hsv = rgb_to_hsv(rgb_norm)

    h = hsv[:, :, 0] * 360.0
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    total_px = h.size

    green_px = ((h >= 55) & (h <= 165) & (s > 0.12) & (v > 0.10)).sum()
    yellow_px = ((h >= 30) & (h < 60) & (s > 0.15) & (v > 0.25)).sum()
    brown_px = ((h >= 0) & (h < 35) & (s > 0.12) & (v > 0.10) & (v < 0.85)).sum()

    plant_ratio = (green_px + yellow_px + brown_px) / total_px
    strong_green_ratio = ((h >= 60) & (h <= 150) & (s > 0.18)).sum() / total_px
    strong_yellow_ratio = ((h >= 30) & (h < 60) & (s > 0.18)).sum() / total_px

    if plant_ratio < 0.12:
        return False
    if strong_green_ratio < 0.03 and strong_yellow_ratio > 0.55:
        return False
    if strong_green_ratio < 0.04 and brown_px / total_px < 0.03 and yellow_px / total_px < 0.15:
        return False

    return True


def safe_pie_values(values):
    arr = np.array(values, dtype=float)
    if np.sum(arr) <= 0:
        return [34.0, 33.0, 33.0]
    arr = np.maximum(arr, 0.5)
    arr = arr / np.sum(arr) * 100.0
    return arr.tolist()


def get_severity(result, confidence, condition):
    if result == "GOOD":
        if confidence >= 86:
            return "Low Risk", "sev-low"
        return "Monitor", "sev-medium"
    if condition == "Disease Detected" or confidence >= 82:
        return "High Risk", "sev-high"
    if confidence >= 68:
        return "Medium Risk", "sev-medium"
    return "Low Risk", "sev-low"


def analyze_leaf(image):
    img = np.array(image.convert("RGB")).astype(np.float32)
    rgb_norm = img / 255.0
    hsv = rgb_to_hsv(rgb_norm)
    h = hsv[:, :, 0] * 360.0
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    candidate = (s > 0.12) & (v > 0.18) & ((h <= 120) | (h >= 335))
    if candidate.mean() < 0.03:
        candidate = (s > 0.08) & (v > 0.15) & ((h <= 130) | (h >= 330))
    if candidate.mean() < 0.02:
        candidate = np.ones_like(h, dtype=bool)

    green_mask = candidate & (h >= 60) & (h <= 160) & (s > 0.18)
    yellow_mask = candidate & (h >= 22) & (h < 60) & (s > 0.15)
    brown_mask = candidate & (
        (((h < 22) | (h >= 335)) & (v < 0.90)) |
        ((s < 0.32) & (v < 0.75))
    )

    green_count = int(green_mask.sum())
    yellow_count = int(yellow_mask.sum())
    brown_count = int(brown_mask.sum())
    candidate_count = int(candidate.sum())

    unclassified = max(candidate_count - green_count - yellow_count - brown_count, 0)

    green_score = green_count + 0.55 * unclassified
    yellow_score = yellow_count + 0.25 * unclassified
    brown_score = brown_count + 0.20 * unclassified

    scores = np.array([green_score, yellow_score, brown_score], dtype=float)
    pie_values = safe_pie_values(scores)

    total_score = float(scores.sum())
    if total_score <= 0:
        green_ratio = yellow_ratio = brown_ratio = 1 / 3
    else:
        green_ratio = float(scores[0] / total_score)
        yellow_ratio = float(scores[1] / total_score)
        brown_ratio = float(scores[2] / total_score)

    brightness = float(np.mean(v[candidate])) if candidate.any() else float(np.mean(v))

    if green_ratio >= 0.62 and brown_ratio < 0.08 and yellow_ratio < 0.18:
        result = "GOOD"
        condition = "Healthy Leaf"
        confidence = 72 + 18 * green_ratio + 10 * brightness + 18 * (green_ratio - max(yellow_ratio, brown_ratio))
    elif brown_ratio >= 0.22:
        result = "BAD"
        condition = "Disease Detected"
        confidence = 65 + 25 * brown_ratio + 10 * (brown_ratio - green_ratio) + 5 * (1 - brightness)
    elif yellow_ratio >= 0.22:
        result = "BAD"
        condition = "Nutrient Deficiency"
        confidence = 62 + 25 * yellow_ratio + 12 * (yellow_ratio - green_ratio) + 5 * (1 - brightness)
    elif green_ratio >= 0.48:
        result = "GOOD"
        condition = "Mostly Healthy"
        confidence = 68 + 20 * green_ratio + 8 * (green_ratio - max(yellow_ratio, brown_ratio)) + 6 * brightness
    else:
        result = "BAD"
        condition = "Mixed Stress"
        confidence = 58 + 20 * max(yellow_ratio, brown_ratio) + 8 * (max(yellow_ratio, brown_ratio) - green_ratio) + 4 * (1 - brightness)

    confidence = round(float(np.clip(confidence, 50.0, 99.9)), 2)
    return result, confidence, condition, pie_values


def treatment_for_condition(condition):
    return TREATMENTS.get(condition, TREATMENTS["Mixed Stress"])


def make_pie_figure(values, colors, labels):
    fig, ax = plt.subplots(figsize=(4.5, 4.5), facecolor="#0f1a10")
    ax.set_facecolor("#0f1a10")

    values = safe_pie_values(values)

    wedges, _, autotexts = ax.pie(
        values,
        autopct=lambda p: f"{p:.1f}%" if p >= 4 else "",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "#0f1a10", "linewidth": 2},
        pctdistance=0.72,
        labels=None,
    )

    legend = ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False,
    )

    for text in legend.get_texts():
        text.set_color("#d5e3f0")

    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(10)

    ax.axis("equal")
    return fig


def figure_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


if REPORTLAB_AVAILABLE:
    def build_report_story(item, styles):
        story = []
        story.append(Paragraph(f"<b>{item['name']}</b>", styles["Title"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Result: {item['result']}", styles["Normal"]))
        story.append(Paragraph(f"Confidence: {item['confidence']}%", styles["Normal"]))
        story.append(Paragraph(f"Condition: {item['condition']}", styles["Normal"]))
        story.append(Paragraph(f"Timestamp: {item.get('timestamp', '—')}", styles["Normal"]))
        story.append(Spacer(1, 10))

        img_buf = io.BytesIO(item["image_bytes"])
        img_buf.seek(0)
        story.append(RLImage(img_buf, width=200, height=200))
        story.append(Spacer(1, 10))

        pie_fig = make_pie_figure(
            item["pie_values"],
            ["#14b8a6", "#f59e0b", "#fb7185"],
            ["Green", "Yellow", "Brown"],
        )
        pie_buf = figure_to_bytes(pie_fig)
        story.append(RLImage(pie_buf, width=200, height=200))
        return story


    def build_pdf_bytes(item):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        doc.build(build_report_story(item, styles))
        buffer.seek(0)
        return buffer.getvalue()


    def build_all_pdf_bytes(history):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        for idx, item in enumerate(history):
            story.extend(build_report_story(item, styles))
            if idx < len(history) - 1:
                story.append(PageBreak())

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
else:
    def build_report_bytes(item):
        text = (
            f"AgroVision AI Report\n\n"
            f"Name: {item['name']}\n"
            f"Result: {item['result']}\n"
            f"Confidence: {item['confidence']}%\n"
            f"Condition: {item['condition']}\n"
            f"Timestamp: {item.get('timestamp', '—')}\n"
        )
        return text.encode("utf-8")


    def build_all_report_bytes(history):
        parts = []
        for item in history:
            parts.append(
                f"AgroVision AI Report\n"
                f"Name: {item['name']}\n"
                f"Result: {item['result']}\n"
                f"Confidence: {item['confidence']}%\n"
                f"Condition: {item['condition']}\n"
                f"Timestamp: {item.get('timestamp', '—')}\n"
                f"{'-'*40}\n"
            )
        return "\n".join(parts).encode("utf-8")


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(
    """
<div class="hero-card">
    <div style="font-family:Sora, sans-serif; font-size:2.1rem; font-weight:700; color:#eef6ff;">
        🌿 AgroVision AI
    </div>
    <div style="font-size:1rem; color:#76d1ff; margin-top:0.35rem;">
        Smart leaf analysis with clean reporting and history tracking
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────
st.sidebar.markdown("### 🌿 AgroVision AI")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
if st.sidebar.button("📁 History"):
    st.session_state.page = "History"
if st.sidebar.button("📊 Analytics"):
    st.session_state.page = "Analytics"
if st.sidebar.button("ℹ️ About"):
    st.session_state.page = "About"

# ─────────────────────────────────────────
# HOME
# ─────────────────────────────────────────
if st.session_state.page == "Home":
    if st.session_state.flash_message:
        st.success(st.session_state.flash_message)
        st.session_state.flash_message = ""

    st.markdown("#### 🔎 Scan a leaf to detect plant health")

    source = st.radio(
        "Input source",
        ["📁 Upload Image", "📷 Use Camera"],
        horizontal=True,
        label_visibility="collapsed",
    )

    image = None
    uploaded_bytes = None

    if source == "📁 Upload Image":
        f = st.file_uploader("Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if f:
            uploaded_bytes = f.getvalue()
            image = Image.open(io.BytesIO(uploaded_bytes))
    else:
        cam = st.camera_input("Point your camera at the leaf and press capture")
        if cam:
            uploaded_bytes = cam.getvalue()
            image = Image.open(io.BytesIO(uploaded_bytes))

    if image and uploaded_bytes:
        if not is_leaf(image):
            st.image(image, use_container_width=True, caption="Uploaded Image")
            st.markdown("Please upload a leaf image.")
            st.stop()

        file_hash = hashlib.sha256(uploaded_bytes).hexdigest()
        result, confidence, condition, pie_values = analyze_leaf(image)
        severity_label, severity_class = get_severity(result, confidence, condition)
        t = treatment_for_condition(condition)

        col_img, col_result = st.columns([1, 1], gap="large")

        with col_img:
            st.image(image, use_container_width=True, caption="Scanned Leaf")

        with col_result:
            st.markdown("##### 🔬 Analysis Result")

            badge_class = "good-badge" if result == "GOOD" else "bad-badge"
            icon = "✅" if result == "GOOD" else "⚠️"
            st.markdown(
                f"<span class='{badge_class}'>{icon} {result}</span>"
                f"&nbsp;&nbsp;<span class='{severity_class}'>{severity_label}</span>",
                unsafe_allow_html=True,
            )
            st.write("")
            st.markdown(f"**Condition:** {condition}")
            st.progress(min(int(confidence), 100))
            st.caption(f"Confidence: **{confidence}%**")

            st.write("")
            p1, p2, p3 = st.columns(3)
            p1.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#a5d6a7'>{pie_values[0]:.0f}%</div>"
                f"<div class='metric-label'>Healthy Tissue</div></div>",
                unsafe_allow_html=True,
            )
            p2.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#ffcc80'>{pie_values[1]:.0f}%</div>"
                f"<div class='metric-label'>Warning Tissue</div></div>",
                unsafe_allow_html=True,
            )
            p3.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#ef9a9a'>{pie_values[2]:.0f}%</div>"
                f"<div class='metric-label'>Damaged Tissue</div></div>",
                unsafe_allow_html=True,
            )

        st.write("---")

        tips_html = "".join(f"<li style='margin-bottom:6px'>{tip}</li>" for tip in t["tips"])
        card_class = f"treatment-card {t['card_class']}".strip()
        st.markdown(f"""
        <div class='{card_class}'>
            <b style='font-family:Sora,sans-serif;color:#e8f5e9;font-size:1rem'>
                {t["icon"]} {t["title"]}
            </b>
            <ul style='color:#c8e6c9;margin-top:10px;padding-left:18px'>
                {tips_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")

        st.markdown("#### 📊 Leaf Colour Composition")
        fig = make_pie_figure(
            pie_values,
            ["#4caf50", "#ffca28", "#8d6e63"],
            ["Green", "Yellow", "Brown"],
        )
        st.pyplot(fig)
        plt.close(fig)

        st.write("---")

        st.markdown("#### 💾 Save Result")
        leaf_name = st.text_input(
            "Leaf scan name",
            placeholder="e.g. Field-A Sample 1",
            key=f"leaf_name_{file_hash}_{st.session_state.save_nonce}",
        )

        if st.button("💾 Save to History"):
            if leaf_name.strip() == "":
                st.write("Please enter a name before saving.")
            elif file_hash in st.session_state.saved_hashes:
                st.write("This image is already saved.")
            else:
                st.session_state.history.append(
                    {
                        "name": leaf_name.strip(),
                        "result": result,
                        "confidence": confidence,
                        "condition": condition,
                        "severity": severity_label,
                        "green": pie_values[0],
                        "yellow": pie_values[1],
                        "brown": pie_values[2],
                        "pie_values": pie_values,
                        "image_bytes": uploaded_bytes,
                        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        "scan_hash": file_hash,
                    }
                )
                st.session_state.saved_hashes.append(file_hash)
                st.session_state.save_nonce += 1
                st.session_state.flash_message = f"✅ '{leaf_name}' saved to history!"
                st.session_state.result_data = None
                st.rerun()
    else:
        st.info("⬆️ Upload an image above to scan a leaf.")

# ─────────────────────────────────────────
# HISTORY
# ─────────────────────────────────────────
elif st.session_state.page == "History":
    st.markdown(
        """
<div class="hero-card">
    <div style="font-family:Sora, sans-serif; font-size:2.0rem; font-weight:700; color:#eef6ff;">
        📁 History
    </div>
    <div style="font-size:1rem; color:#76d1ff; margin-top:0.25rem;">
        Saved analyses with downloadable reports
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.info("No history yet. Save scans from the Home tab.")
    else:
        if st.button("🗑️ Clear All History"):
            st.session_state.history = []
            st.session_state.saved_hashes = []
            st.session_state.result_data = None
            st.rerun()

        for idx, item in enumerate(st.session_state.history, 1):
            badge = "good-badge" if item["result"] == "GOOD" else "bad-badge"
            sev = item.get("severity", "")
            ts = item.get("timestamp", "—")
            sev_class = "sev-low" if "Low" in sev else ("sev-medium" if "Medium" in sev else "sev-high")
            t_data = treatment_for_condition(item.get("condition", "Mixed Stress"))
            tips_html = "".join(
                f"<li style='margin-bottom:4px;color:#a5c9a7;font-size:0.82rem'>{tip}</li>"
                for tip in t_data["tips"]
            )

            st.markdown(
                f"""
<div class='history-card'>
    <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px'>
        <b style='font-size:1rem;font-family:Sora,sans-serif;color:#eef6ff'>
            #{idx} — {item['name']}
        </b>
        <span class='small-note'>🕐 {ts}</span>
    </div>
    <br>
    <span class='{badge}'>{item['result']}</span>
    &nbsp;<span class='{sev_class}'>{sev if sev else "—"}</span>
    &nbsp;&nbsp;
    <span style='color:#cfe8ff'>Condition: {item['condition']}</span><br>
    <span style='color:#76d1ff;font-size:0.85rem'>Confidence: {item['confidence']}%</span>
</div>
""",
                unsafe_allow_html=True,
            )

            if REPORTLAB_AVAILABLE:
                report_bytes = build_pdf_bytes(item)
                file_name = f"{item['name']}.pdf"
            else:
                report_bytes = build_report_bytes(item)
                file_name = f"{item['name']}.txt"

            st.download_button(
                "Download Report",
                report_bytes,
                file_name=file_name,
                key=f"download_{idx}",
            )

        st.markdown("---")

        if REPORTLAB_AVAILABLE:
            all_report = build_all_pdf_bytes(st.session_state.history)
            all_name = "All_Leaf_Reports.pdf"
        else:
            all_report = build_all_report_bytes(st.session_state.history)
            all_name = "All_Leaf_Reports.txt"

        st.download_button(
            "Download All Reports",
            all_report,
            file_name=all_name,
        )

# ─────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────
elif st.session_state.page == "Analytics":
    st.markdown(
        """
<div class="hero-card">
    <div style="font-family:Sora, sans-serif; font-size:2.0rem; font-weight:700; color:#eef6ff;">
        📊 Analytics
    </div>
    <div style="font-size:1rem; color:#76d1ff; margin-top:0.25rem;">
        Overall scan trends and health summary
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.history:
        good_count = sum(1 for i in st.session_state.history if i["result"] == "GOOD")
        bad_count = sum(1 for i in st.session_state.history if i["result"] == "BAD")
        high_risk = sum(1 for i in st.session_state.history if "High" in i.get("severity", ""))
        total = len(st.session_state.history)

        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(
            f"<div class='metric-box'><div class='metric-num'>{total}</div><div class='metric-label'>Total Scans</div></div>",
            unsafe_allow_html=True,
        )
        m2.markdown(
            f"<div class='metric-box'><div class='metric-num' style='color:#a5d6a7'>{good_count}</div><div class='metric-label'>Healthy</div></div>",
            unsafe_allow_html=True,
        )
        m3.markdown(
            f"<div class='metric-box'><div class='metric-num' style='color:#ef9a9a'>{bad_count}</div><div class='metric-label'>Diseased / Deficient</div></div>",
            unsafe_allow_html=True,
        )
        m4.markdown(
            f"<div class='metric-box'><div class='metric-num' style='color:#ef5350'>{high_risk}</div><div class='metric-label'>High Risk</div></div>",
            unsafe_allow_html=True,
        )

        st.write("")
        col_pie, col_bar = st.columns(2)

        with col_pie:
            st.markdown("##### Health Distribution")
            fig2, ax2 = plt.subplots(figsize=(4, 4), facecolor="#0f1a10")
            ax2.set_facecolor("#0f1a10")
            ax2.pie(
                [good_count, bad_count],
                labels=["GOOD", "BAD"],
                autopct="%1.1f%%",
                colors=["#4caf50", "#ef5350"],
                startangle=90,
                wedgeprops={"edgecolor": "#0f1a10", "linewidth": 2},
            )
            for tx in ax2.texts:
                tx.set_color("#c8e6c9")
            st.pyplot(fig2)
            plt.close(fig2)

        with col_bar:
            st.markdown("##### Confidence per Scan")
            names = [
                entry["name"][:12] if entry["name"] else f"Scan {i+1}"
                for i, entry in enumerate(st.session_state.history)
            ]
            confidences = [entry["confidence"] for entry in st.session_state.history]
            bar_colors = ["#4caf50" if entry["result"] == "GOOD" else "#ef5350" for entry in st.session_state.history]

            fig3, ax3 = plt.subplots(figsize=(5, 4), facecolor="#0f1a10")
            ax3.set_facecolor("#1a2b1c")
            ax3.bar(range(len(names)), confidences, color=bar_colors, edgecolor="#0f1a10")
            ax3.set_xticks(range(len(names)))
            ax3.set_xticklabels(names, rotation=30, ha="right", color="#c8e6c9", fontsize=9)
            ax3.set_ylabel("Confidence (%)", color="#c8e6c9", fontsize=9)
            ax3.set_ylim(0, 100)
            ax3.tick_params(colors="#c8e6c9")
            for spine in ax3.spines.values():
                spine.set_edgecolor("#2d4a2f")
            ax3.legend(
                handles=[
                    mpatches.Patch(color="#4caf50", label="GOOD"),
                    mpatches.Patch(color="#ef5350", label="BAD"),
                ],
                facecolor="#1a2b1c",
                labelcolor="white",
                edgecolor="#2d4a2f",
            )
            st.pyplot(fig3)
            plt.close(fig3)

        st.write("")
        st.markdown("##### 🌡️ Severity Breakdown")

        sev_counts = {
            "Low Risk": sum(1 for i in st.session_state.history if "Low" in i.get("severity", "")),
            "Medium Risk": sum(1 for i in st.session_state.history if "Medium" in i.get("severity", "")),
            "High Risk": sum(1 for i in st.session_state.history if "High" in i.get("severity", "")),
        }

        fig4, ax4 = plt.subplots(figsize=(5, 2.5), facecolor="#0f1a10")
        ax4.set_facecolor("#1a2b1c")
        bars = ax4.barh(
            list(sev_counts.keys()),
            list(sev_counts.values()),
            color=["#4caf50", "#ffa726", "#ef5350"],
            edgecolor="#0f1a10",
            height=0.5,
        )
        ax4.set_xlabel("Count", color="#c8e6c9", fontsize=9)
        ax4.tick_params(colors="#c8e6c9")
        for spine in ax4.spines.values():
            spine.set_edgecolor("#2d4a2f")
        for bar, val in zip(bars, sev_counts.values()):
            ax4.text(
                bar.get_width() + 0.05,
                bar.get_y() + bar.get_height() / 2,
                str(val),
                va="center",
                color="white",
                fontsize=10,
            )
        st.pyplot(fig4)
        plt.close(fig4)
    else:
        st.info("No scan data yet. Upload and save leaf images from the Dashboard tab.")

# ─────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────
elif st.session_state.page == "About":
    st.markdown(
        """
<div class="hero-card">
    <div style="font-family:Sora, sans-serif; font-size:2.0rem; font-weight:700; color:#eef6ff;">
        ℹ️ About AgroVision AI
    </div>
    <div style="font-size:1rem; color:#76d1ff; margin-top:0.25rem;">
        Smart plant leaf analysis system
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown(
            """
<div class='about-card'>
    <h4 style='margin-top:0;color:#76d1ff'>🌿 What It Does</h4>
    AgroVision AI analyses leaf images using colour-ratio intelligence to detect plant health.
    It provides a clear health result, confidence score, pie chart analysis, and downloadable reports.
</div>
<div class='about-card'>
    <h4 style='margin-top:0;color:#76d1ff'>🚀 Features</h4>
    • Leaf health detection<br>
    • Confidence-based prediction<br>
    • Visual pie chart analysis<br>
    • History tracking<br>
    • Report downloads
</div>
""",
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown(
            """
<div class='about-card'>
    <h4 style='margin-top:0;color:#76d1ff'>🔬 How It Works</h4>
    The model checks colour ratios from the uploaded leaf image and uses them to determine
    whether the leaf is healthy, diseased, or stressed.
</div>
<div class='about-card'>
    <h4 style='margin-top:0;color:#76d1ff'>🔮 Future Scope</h4>
    • Deep learning based disease detection<br>
    • Weather and soil integration<br>
    • Mobile app support<br>
    • Crop-specific disease classification
</div>
""",
            unsafe_allow_html=True,
        )
