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
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# CSS
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

.hero-card, .main-card, .stat-card, .history-card, .about-card {
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
if "flash_message" not in st.session_state:
    st.session_state.flash_message = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def is_leaf(image: Image.Image) -> bool:
    img = np.array(image.convert("RGB")).astype(np.float32)
    hsv = rgb_to_hsv(img / 255.0)

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


def make_pie_figure(values, colors, labels):
    fig, ax = plt.subplots(figsize=(4.5, 4.5), facecolor="#0c1722")
    ax.set_facecolor("#0c1722")

    wedges, _, autotexts = ax.pie(
        safe_pie_values(values),
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "#0c1722", "linewidth": 2},
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
    return {
        "Healthy Leaf": {},
        "Mostly Healthy": {},
        "Disease Detected": {},
        "Nutrient Deficiency": {},
        "Mixed Stress": {},
    }.get(condition, {})


def make_report_bytes(item):
    if REPORTLAB_AVAILABLE:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

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

        pie_fig = make_pie_figure(item["pie_values"], ["#4caf50", "#ffca28", "#8d6e63"], ["Green", "Yellow", "Brown"])
        pie_buf = figure_to_bytes(pie_fig)
        story.append(RLImage(pie_buf, width=200, height=200))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    text = (
        f"AgroVision AI Report\n\n"
        f"Name: {item['name']}\n"
        f"Result: {item['result']}\n"
        f"Confidence: {item['confidence']}%\n"
        f"Condition: {item['condition']}\n"
        f"Timestamp: {item.get('timestamp', '—')}\n"
    )
    return text.encode("utf-8")


def make_all_report_bytes(history):
    if REPORTLAB_AVAILABLE:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        for idx, item in enumerate(history):
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

            pie_fig = make_pie_figure(item["pie_values"], ["#4caf50", "#ffca28", "#8d6e63"], ["Green", "Yellow", "Brown"])
            pie_buf = figure_to_bytes(pie_fig)
            story.append(RLImage(pie_buf, width=200, height=200))

            if idx < len(history) - 1:
                story.append(PageBreak())

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

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
        Green, Yellow, Brown ratio analysis
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

    st.markdown("#### 🔎 Scan a leaf image")

    image = None
    uploaded_bytes = None

    f = st.file_uploader("Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if f:
        uploaded_bytes = f.getvalue()
        image = Image.open(io.BytesIO(uploaded_bytes))

    if image and uploaded_bytes:
        if not is_leaf(image):
            st.image(image, use_container_width=True, caption="Uploaded Image")
            st.write("Please upload a valid leaf image.")
            st.stop()

        file_hash = hashlib.sha256(uploaded_bytes).hexdigest()

        result, confidence, condition, pie_values = analyze_leaf(image)
        severity_label, severity_class = get_severity(result, confidence, condition)

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
            c1, c2, c3 = st.columns(3)
            c1.markdown(
                f"<div class='stat-card'><div class='soft-label'>Green Ratio</div><div class='soft-value' style='color:#a5d6a7'>{pie_values[0]:.0f}%</div></div>",
                unsafe_allow_html=True,
            )
            c2.markdown(
                f"<div class='stat-card'><div class='soft-label'>Yellow Ratio</div><div class='soft-value' style='color:#ffcc80'>{pie_values[1]:.0f}%</div></div>",
                unsafe_allow_html=True,
            )
            c3.markdown(
                f"<div class='stat-card'><div class='soft-label'>Brown Ratio</div><div class='soft-value' style='color:#ef9a9a'>{pie_values[2]:.0f}%</div></div>",
                unsafe_allow_html=True,
            )

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

        leaf_name = st.text_input(
            "Leaf scan name",
            placeholder="e.g. Field-A Sample 1",
            key=f"leaf_name_{file_hash}_{st.session_state.save_nonce}",
        )

        if st.button("💾 Save to History"):
            save_name = leaf_name.strip() if leaf_name.strip() else f"Leaf Scan {len(st.session_state.history)+1}"

            if file_hash in st.session_state.saved_hashes:
                st.write("This leaf image is already saved in history.")
            else:
                st.session_state.history.append(
                    {
                        "name": save_name,
                        "result": result,
                        "confidence": confidence,
                        "condition": condition,
                        "severity": severity_label,
                        "pie_values": pie_values,
                        "image_bytes": uploaded_bytes,
                        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        "scan_hash": file_hash,
                    }
                )
                st.session_state.saved_hashes.append(file_hash)
                st.session_state.save_nonce += 1
                st.session_state.flash_message = f"Saved: {save_name}"
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
        Saved scans
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

            report_bytes = make_report_bytes(item)
            file_name = f"{item['name']}.pdf" if REPORTLAB_AVAILABLE else f"{item['name']}.txt"

            st.download_button(
                "Download Report",
                report_bytes,
                file_name=file_name,
                key=f"download_{idx}",
            )

        st.markdown("---")

        all_report = make_all_report_bytes(st.session_state.history)
        all_name = "All_Leaf_Reports.pdf" if REPORTLAB_AVAILABLE else "All_Leaf_Reports.txt"

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
        Scan summary
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.history:
        green_count = sum(1 for i in st.session_state.history if i["result"] == "GOOD")
        bad_count = sum(1 for i in st.session_state.history if i["result"] == "BAD")
        total = len(st.session_state.history)

        m1, m2, m3 = st.columns(3)
        m1.markdown(
            f"<div class='stat-card'><div class='soft-label'>Total Scans</div><div class='soft-value'>{total}</div></div>",
            unsafe_allow_html=True,
        )
        m2.markdown(
            f"<div class='stat-card'><div class='soft-label'>GOOD</div><div class='soft-value' style='color:#99f6e4'>{green_count}</div></div>",
            unsafe_allow_html=True,
        )
        m3.markdown(
            f"<div class='stat-card'><div class='soft-label'>BAD</div><div class='soft-value' style='color:#fecaca'>{bad_count}</div></div>",
            unsafe_allow_html=True,
        )

        st.write("")
        col_pie, col_bar = st.columns(2)

        with col_pie:
            st.markdown("##### Good vs Bad")
            fig2, ax2 = plt.subplots(figsize=(4, 4), facecolor="#0f1a10")
            ax2.set_facecolor("#0f1a10")
            ax2.pie(
                [green_count, bad_count],
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
            names = [entry["name"][:12] if entry["name"] else f"Scan {i+1}" for i, entry in enumerate(st.session_state.history)]
            confidences = [entry["confidence"] for entry in st.session_state.history]
            bar_colors = ["#4caf50" if entry["result"] == "GOOD" else "#ef5350" for entry in st.session_state.history]

            fig3, ax3 = plt.subplots(figsize=(5, 4), facecolor="#0f1a10")
            ax3.set_facecolor("#1a2b1c")
            ax3.bar(range(len(names)), confidences, color=bar_colors, edgecolor="#0f1a10")
            ax3.set_xticks(range(len(names)))
            ax3.set_xticklabels(names, rotation=30, ha="right", color="#d5e3f0", fontsize=9)
            ax3.set_ylabel("Confidence (%)", color="#d5e3f0", fontsize=9)
            ax3.set_ylim(0, 100)
            ax3.tick_params(colors="#d5e3f0")
            for spine in ax3.spines.values():
                spine.set_edgecolor("#23405c")
            ax3.legend(
                handles=[
                    mpatches.Patch(color="#4caf50", label="GOOD"),
                    mpatches.Patch(color="#ef5350", label="BAD"),
                ],
                facecolor="#0c1722",
                labelcolor="white",
                edgecolor="#23405c",
            )
            st.pyplot(fig3)
            plt.close(fig3)
    else:
        st.info("No scan data yet. Upload and save leaf images from the Home tab.")

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
        Green, Yellow, Brown ratio analysis
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown(
            """
<div class="about-card">
    <h4 style="margin-top:0;color:#76d1ff">🌿 What It Does</h4>
    AgroVision AI checks the green, yellow, and brown ratio in a leaf image.
</div>
<div class="about-card">
    <h4 style="margin-top:0;color:#76d1ff">🚀 Features</h4>
    • Green ratio<br>
    • Yellow ratio<br>
    • Brown ratio<br>
    • History tracking<br>
    • Report downloads
</div>
""",
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown(
            """
<div class="about-card">
    <h4 style="margin-top:0;color:#76d1ff">🔬 How It Works</h4>
    The model reads the uploaded image and checks the color ratios.
</div>
<div class="about-card">
    <h4 style="margin-top:0;color:#76d1ff">🔮 Future Scope</h4>
    • Better ratio analysis<br>
    • More leaf samples<br>
    • Mobile app support<br>
    • Crop-specific scanning
</div>
""",
            unsafe_allow_html=True,
    )
