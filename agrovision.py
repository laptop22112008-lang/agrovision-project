import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import rgb_to_hsv
from datetime import datetime
import io
import hashlib

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# CONFIG
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
st.set_page_config(
    page_title="AgroVision AI",
    page_icon="\ud83c\udf3f",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# CUSTOM CSS
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 3rem; }

/* Box tab navigation */
div[data-baseweb="tab-list"] {
    gap: 8px; background: transparent;
    border-bottom: none !important; flex-wrap: wrap;
}
div[data-baseweb="tab"] {
    background: #1e2d1f; border: 1.5px solid #2e4d30;
    border-radius: 10px !important; padding: 10px 22px !important;
    font-family: 'Sora', sans-serif; font-size: 0.88rem;
    font-weight: 600; color: #a5c9a7 !important;
    transition: all 0.2s ease; white-space: nowrap;
}
div[data-baseweb="tab"]:hover {
    background: #2a4a2c; border-color: #4caf50; color: #fff !important;
}
div[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    border-color: #66bb6a !important; color: #fff !important;
    box-shadow: 0 4px 14px rgba(76,175,80,0.35);
}
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }

/* Cards */
.agro-card {
    background: #1a2b1c; border: 1px solid #2d4a2f;
    border-radius: 14px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}

/* Hero */
.hero-wrap {
    width: 100%;
    text-align: center;
    margin-bottom: 1rem;
    padding: 1.2rem 0.5rem 0 0.5rem;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(1.55rem, 4.5vw, 2.45rem);
    font-weight: 700;
    color: #e8f5e9;
    letter-spacing: -0.5px;
    margin: 0 auto;
    line-height: 1.08;
    word-break: break-word;
    overflow-wrap: anywhere;
    max-width: 100%;
}
.hero-sub {
    font-size: 1rem; color: #81c784;
    margin-top: 6px; margin-bottom: 0;
}

/* Result badges */
.badge-good {
    display: inline-block; background: #1b5e20; border: 1.5px solid #43a047;
    color: #a5d6a7; border-radius: 8px; padding: 6px 18px;
    font-weight: 700; font-family: 'Sora', sans-serif; font-size: 1.1rem;
}
.badge-bad {
    display: inline-block; background: #5e1b1b; border: 1.5px solid #e53935;
    color: #ef9a9a; border-radius: 8px; padding: 6px 18px;
    font-weight: 700; font-family: 'Sora', sans-serif; font-size: 1.1rem;
}

/* Severity badges */
.sev-low {
    display: inline-block; background: #1b3a1f; border: 1.5px solid #43a047;
    color: #a5d6a7; border-radius: 20px; padding: 4px 16px;
    font-weight: 600; font-family: 'Sora', sans-serif; font-size: 0.85rem;
}
.sev-medium {
    display: inline-block; background: #3e2a00; border: 1.5px solid #ffa726;
    color: #ffcc80; border-radius: 20px; padding: 4px 16px;
    font-weight: 600; font-family: 'Sora', sans-serif; font-size: 0.85rem;
}
.sev-high {
    display: inline-block; background: #5e1b1b; border: 1.5px solid #ef5350;
    color: #ef9a9a; border-radius: 20px; padding: 4px 16px;
    font-weight: 600; font-family: 'Sora', sans-serif; font-size: 0.85rem;
}

/* Treatment cards */
.treatment-card {
    background: #0f2211; border: 1px solid #2d6a35;
    border-left: 4px solid #43a047;
    border-radius: 10px; padding: 1rem 1.2rem; margin-top: 0.6rem;
}
.treatment-card.warn {
    background: #1e1400; border: 1px solid #6d4c00;
    border-left: 4px solid #ffa726;
}
.treatment-card.danger {
    background: #1e0a0a; border: 1px solid #6d1212;
    border-left: 4px solid #ef5350;
}

/* Metric tiles */
.metric-box {
    background: #1a2b1c; border: 1px solid #2d4a2f;
    border-radius: 12px; padding: 1rem; text-align: center;
}
.metric-num { font-family: 'Sora', sans-serif; font-size: 2rem; font-weight: 700; color: #a5d6a7; }
.metric-label { font-size: 0.8rem; color: #81c784; margin-top: 2px; }

/* Timestamp */
.ts-tag { font-size: 0.75rem; color: #558b57; font-style: italic; }

/* Global overrides */
body { background-color: #0f1a10; color: #e0e0e0; }
h1, h2, h3 { font-family: 'Sora', sans-serif; color: #e8f5e9; }
.stButton>button {
    background: linear-gradient(135deg, #2e7d32, #43a047);
    color: white; border: none; border-radius: 8px;
    padding: 0.5rem 1.4rem; font-family: 'Sora', sans-serif;
    font-weight: 600; transition: 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #388e3c, #66bb6a);
    transform: translateY(-1px); box-shadow: 0 4px 12px rgba(76,175,80,0.4);
}
.stTextInput>div>div>input {
    background: #1a2b1c; border: 1px solid #2d4a2f;
    color: #e0e0e0; border-radius: 8px;
}
.stFileUploader { background: #1a2b1c; border: 1.5px dashed #2d4a2f; border-radius: 12px; }
div[data-testid="stAlert"] { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# SESSION STATE
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if "history" not in st.session_state:
    st.session_state.history = []

if "saved_hashes" not in st.session_state:
    st.session_state.saved_hashes = []

if "save_nonce" not in st.session_state:
    st.session_state.save_nonce = 0

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# TREATMENT DATABASE
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
TREATMENTS = {
    "Healthy Leaf": {
        "card_class": "",
        "icon": "\u2705",
        "title": "Plant is healthy \u2014 maintain current care",
        "tips": [
            "Continue the regular watering schedule",
            "Apply balanced NPK fertiliser monthly",
            "Monitor for early signs of pests or discolouration",
            "Ensure adequate sunlight and airflow between plants",
        ],
    },
    "Mostly Healthy": {
        "card_class": "",
        "icon": "\ud83d\udfe2",
        "title": "Mostly healthy \u2014 only minor stress detected",
        "tips": [
            "Inspect the plant again in 3\u20135 days",
            "Check if the leaf is getting too much direct sun",
            "Avoid overwatering and keep soil moisture stable",
            "Remove only clearly damaged parts if needed",
        ],
    },
    "Disease Detected": {
        "card_class": "danger",
        "icon": "\ud83e\udda0",
        "title": "Disease treatment recommended",
        "tips": [
            "Remove and dispose of heavily infected leaves immediately",
            "Apply a copper-based or neem oil fungicide/bactericide spray",
            "Avoid overhead watering \u2014 water at the base only",
            "Increase plant spacing to improve air circulation",
            "Re-inspect after 7 days and repeat treatment if needed",
        ],
    },
    "Nutrient Deficiency": {
        "card_class": "warn",
        "icon": "\ud83c\udf31",
        "title": "Nutrient correction needed",
        "tips": [
            "Test soil pH \u2014 ideal range is 6.0\u20137.0 for most crops",
            "Apply a micronutrient-rich foliar spray (Fe, Mg, Zn)",
            "Add organic compost to improve soil structure and retention",
            "Consider a slow-release fertiliser with balanced N-P-K",
            "Avoid over-watering which leaches nutrients from the soil",
        ],
    },
    "Mixed Stress": {
        "card_class": "warn",
        "icon": "\u26a0\ufe0f",
        "title": "Mixed stress detected \u2014 monitor carefully",
        "tips": [
            "Check watering consistency first",
            "Inspect for pests, fungal spots, and leaf curling",
            "Reduce heat stress with partial shade if needed",
            "Re-scan the leaf under natural light for confirmation",
            "If symptoms spread, isolate the plant from others",
        ],
    },
}

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# HELPERS
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
def safe_pie_values(values):
    arr = np.array(values, dtype=float)
    total = float(arr.sum())

    if total <= 0:
        return [34.0, 33.0, 33.0]

    if np.max(arr) / total >= 0.995:
        out = [0.0, 0.0, 0.0]
        out[int(np.argmax(arr))] = 100.0
        return out

    arr = np.maximum(arr, 0.5)
    arr = arr / np.sum(arr) * 100.0
    return arr.tolist()


def get_severity(result: str, confidence: float, condition: str):
    if result == "GOOD":
        if confidence >= 86:
            return "\ud83d\udfe2 Low Risk", "sev-low"
        return "\ud83d\udfe1 Monitor", "sev-medium"

    if condition == "Disease Detected" or confidence >= 82:
        return "\ud83d\udd34 High Risk", "sev-high"
    if confidence >= 68:
        return "\ud83d\udfe0 Medium Risk", "sev-medium"
    return "\ud83d\udfe1 Low Risk", "sev-low"


def analyze_leaf(image: Image.Image):
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

    green_mask  = candidate & (h >= 60) & (h <= 160) & (s > 0.18)
    yellow_mask = candidate & (h >= 22) & (h < 60) & (s > 0.15)
    brown_mask  = candidate & (
        (((h < 22) | (h >= 335)) & (v < 0.90)) |
        ((s < 0.32) & (v < 0.75))
    )

    green_count     = int(green_mask.sum())
    yellow_count    = int(yellow_mask.sum())
    brown_count     = int(brown_mask.sum())
    candidate_count = int(candidate.sum())

    unclassified = max(candidate_count - green_count - yellow_count - brown_count, 0)

    green_score  = green_count  + 0.55 * unclassified
    yellow_score = yellow_count + 0.25 * unclassified
    brown_score  = brown_count  + 0.20 * unclassified

    scores     = np.array([green_score, yellow_score, brown_score], dtype=float)
    pie_values = safe_pie_values(scores)

    total_score = float(scores.sum())
    if total_score <= 0:
        green_ratio = yellow_ratio = brown_ratio = 1 / 3
    else:
        green_ratio  = float(scores[0] / total_score)
        yellow_ratio = float(scores[1] / total_score)
        brown_ratio  = float(scores[2] / total_score)

    brightness = float(np.mean(v[candidate])) if candidate.any() else float(np.mean(v))

    if green_ratio >= 0.62 and brown_ratio < 0.08 and yellow_ratio < 0.18:
        result     = "GOOD"
        condition  = "Healthy Leaf"
        confidence = 72 + 18 * green_ratio + 10 * brightness + 18 * (green_ratio - max(yellow_ratio, brown_ratio))
    elif brown_ratio >= 0.22:
        result     = "BAD"
        condition  = "Disease Detected"
        confidence = 65 + 25 * brown_ratio + 10 * (brown_ratio - green_ratio) + 5 * (1 - brightness)
    elif yellow_ratio >= 0.22:
        result     = "BAD"
        condition  = "Nutrient Deficiency"
        confidence = 62 + 25 * yellow_ratio + 12 * (yellow_ratio - green_ratio) + 5 * (1 - brightness)
    elif green_ratio >= 0.48:
        result     = "GOOD"
        condition  = "Mostly Healthy"
        confidence = 68 + 20 * green_ratio + 8 * (green_ratio - max(yellow_ratio, brown_ratio)) + 6 * brightness
    else:
        result     = "BAD"
        condition  = "Mixed Stress"
        confidence = 58 + 20 * max(yellow_ratio, brown_ratio) + 8 * (max(yellow_ratio, brown_ratio) - green_ratio) + 4 * (1 - brightness)

    confidence = round(float(np.clip(confidence, 50.0, 99.9)), 2)
    return result, confidence, condition, pie_values


def treatment_for_condition(condition: str):
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


# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# HEADER
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">\ud83c\udf3f AgroVision AI</div>
    <div class="hero-sub">Smart Plant Health Intelligence</div>
</div>
""", unsafe_allow_html=True)

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# NAVIGATION
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
tab_dashboard, tab_analytics, tab_history, tab_about = st.tabs(
    ["\ud83c\udfe0  Dashboard", "\ud83d\udcca  Analytics", "\ud83d\udcc1  History", "\u2139\ufe0f  About"]
)

# \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
# DASHBOARD
# \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
with tab_dashboard:
    st.markdown("#### \ud83d\udd0e Scan a leaf to detect plant health")

    source = st.radio(
        "Input source",
        ["\ud83d\udcc1 Upload Image", "\ud83d\udcf7 Use Camera"],
        horizontal=True,
        label_visibility="collapsed"
    )

    image         = None
    uploaded_bytes = None

    if source == "\ud83d\udcc1 Upload Image":
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
        file_hash = hashlib.sha256(uploaded_bytes).hexdigest()
        result, confidence, condition, pie_values = analyze_leaf(image)
        severity_label, severity_class = get_severity(result, confidence, condition)
        t = treatment_for_condition(condition)

        col_img, col_result = st.columns([1, 1], gap="large")

        with col_img:
            st.image(image, use_container_width=True, caption="Scanned Leaf")

        with col_result:
            st.markdown("##### \ud83d\udd2c Analysis Result")

            badge_class = "badge-good" if result == "GOOD" else "badge-bad"
            icon = "\u2705" if result == "GOOD" else "\u26a0\ufe0f"
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

        tips_html  = "".join(f"<li style='margin-bottom:6px'>{tip}</li>" for tip in t["tips"])
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

        st.markdown("#### \ud83d\udcca Leaf Colour Composition")
        fig = make_pie_figure(
            pie_values,
            ["#4caf50", "#ffca28", "#8d6e63"],
            ["Green", "Yellow", "Brown"],
        )
        st.pyplot(fig)
        plt.close(fig)

        st.write("---")

        st.markdown("#### \ud83d\udcbe Save Result")
        leaf_name = st.text_input(
            "Leaf scan name",
            placeholder="e.g. Field-A Sample 1",
            key=f"leaf_name_{file_hash}_{st.session_state.save_nonce}",
        )

        if st.button("\ud83d\udcbe Save to History"):
            if leaf_name.strip() == "":
                st.warning("Please enter a name before saving.")
            elif file_hash in st.session_state.saved_hashes:
                st.warning("This image is already saved.")
            else:
                st.session_state.history.append({
                    "name":        leaf_name.strip(),
                    "result":      result,
                    "confidence":  confidence,
                    "condition":   condition,
                    "severity":    severity_label,
                    "pie_values":  pie_values,
                    "image_bytes": uploaded_bytes,
                    "timestamp":   datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "scan_hash":   file_hash,
                })
                st.session_state.saved_hashes.append(file_hash)
                st.session_state.save_nonce += 1
                st.success(f"\u2705 '{leaf_name}' saved to history!")
                st.rerun()
    else:
        st.info("\u2b06\ufe0f Upload an image or use your camera above to scan a leaf.")

# \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
# ANALYTICS
# \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
with tab_analytics:
    st.markdown("#### \ud83d\udcca Scan Analytics")

    if st.session_state.history:
        good_count = sum(1 for i in st.session_state.history if i["result"] == "GOOD")
        bad_count  = sum(1 for i in st.session_state.history if i["result"] == "BAD
