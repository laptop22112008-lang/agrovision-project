import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AgroVision AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 1.5rem; }

/* ── Box tab navigation ── */
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

/* ── Cards ── */
.agro-card {
    background: #1a2b1c; border: 1px solid #2d4a2f;
    border-radius: 14px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Sora', sans-serif; font-size: 2.6rem; font-weight: 700;
    color: #e8f5e9; text-align: center; letter-spacing: -0.5px; margin-bottom: 0;
}
.hero-sub {
    font-size: 1rem; color: #81c784; text-align: center;
    margin-top: 4px; margin-bottom: 1.6rem;
}

/* ── Result badges ── */
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

/* ── Severity badges ── */
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

/* ── Treatment cards ── */
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

/* ── Metric tiles ── */
.metric-box {
    background: #1a2b1c; border: 1px solid #2d4a2f;
    border-radius: 12px; padding: 1rem; text-align: center;
}
.metric-num { font-family: 'Sora', sans-serif; font-size: 2rem; font-weight: 700; color: #a5d6a7; }
.metric-label { font-size: 0.8rem; color: #81c784; margin-top: 2px; }

/* ── Timestamp ── */
.ts-tag { font-size: 0.75rem; color: #558b57; font-style: italic; }

/* ── Global overrides ── */
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

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────
#  TREATMENT DATABASE
# ─────────────────────────────────────────
TREATMENTS = {
    "Healthy Leaf": {
        "card_class": "",
        "icon": "✅",
        "title": "Plant is healthy — maintain current care",
        "tips": [
            "Continue regular watering schedule",
            "Apply balanced NPK fertiliser monthly",
            "Monitor for early signs of pests or discolouration",
            "Ensure adequate sunlight and airflow between plants",
        ]
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
        ]
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
        ]
    }
}

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────

def get_severity(result: str, confidence: float):
    if result == "GOOD":
        return "🟢 Low Risk", "sev-low"
    if confidence >= 55:
        return "🔴 High Risk", "sev-high"
    return "🟡 Medium Risk", "sev-medium"


def analyze_leaf(image: Image.Image):
    img = np.array(image.convert("RGB"))
    r = float(np.mean(img[:, :, 0]))
    g = float(np.mean(img[:, :, 1]))
    b = float(np.mean(img[:, :, 2]))
    total = r + g + b + 1e-6
    green_ratio = g / total
    red_ratio   = r / total

    if green_ratio > 0.38:
        result, condition = "GOOD", "Healthy Leaf"
        confidence = round(min(green_ratio * 100, 99.9), 2)
    elif red_ratio > 0.34:
        result, condition = "BAD", "Disease Detected"
        confidence = round(min(red_ratio * 100, 99.9), 2)
    else:
        result, condition = "BAD", "Nutrient Deficiency"
        confidence = round(min((red_ratio + (1 - green_ratio)) * 50, 99.9), 2)

    return result, confidence, condition, [g, r, b]

# ─────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────
st.markdown("<div class='hero-title'>🌿 AgroVision AI</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Smart Plant Health Intelligence</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────
tab_dashboard, tab_analytics, tab_history, tab_about = st.tabs(
    ["🏠  Dashboard", "📊  Analytics", "📁  History", "ℹ️  About"]
)

# ══════════════════════════════════════════
#  TAB 1 – DASHBOARD
# ══════════════════════════════════════════
with tab_dashboard:
    st.markdown("#### Scan a leaf to detect plant health")

    # ── Input toggle: Upload vs Camera ──
    source = st.radio(
        "Input source", ["📁 Upload Image", "📷 Use Camera"],
        horizontal=True, label_visibility="collapsed"
    )

    image = None
    if source == "📁 Upload Image":
        f = st.file_uploader(
            "Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
        )
        if f:
            image = Image.open(f)
    else:
        cam = st.camera_input("Point your camera at the leaf and press capture")
        if cam:
            image = Image.open(cam)

    if image:
        result, confidence, condition, rgb_values = analyze_leaf(image)
        severity_label, severity_class = get_severity(result, confidence)

        col_img, col_result = st.columns([1, 1], gap="large")

        with col_img:
            st.image(image, use_container_width=True, caption="Scanned Leaf")

        with col_result:
            st.markdown("##### 🔬 Analysis Result")

            badge_class = "badge-good" if result == "GOOD" else "badge-bad"
            icon = "✅" if result == "GOOD" else "⚠️"
            st.markdown(
                f"<span class='{badge_class}'>{icon} {result}</span>"
                f"&nbsp;&nbsp;<span class='{severity_class}'>{severity_label}</span>",
                unsafe_allow_html=True
            )
            st.write("")

            st.markdown(f"**Condition:** {condition}")
            st.progress(min(int(confidence), 100))
            st.caption(f"Confidence: **{confidence}%**")
            st.write("")

            g_val, r_val, b_val = rgb_values
            total_rgb = g_val + r_val + b_val + 1e-6
            c1, c2, c3 = st.columns(3)
            c1.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#a5d6a7'>{g_val/total_rgb*100:.0f}%</div>"
                f"<div class='metric-label'>Green</div></div>", unsafe_allow_html=True
            )
            c2.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#ef9a9a'>{r_val/total_rgb*100:.0f}%</div>"
                f"<div class='metric-label'>Red</div></div>", unsafe_allow_html=True
            )
            c3.markdown(
                f"<div class='metric-box'><div class='metric-num' style='color:#90caf9'>{b_val/total_rgb*100:.0f}%</div>"
                f"<div class='metric-label'>Blue</div></div>", unsafe_allow_html=True
            )

        st.write("---")

        # ── 💡 Treatment Suggestions ──
        t = TREATMENTS[condition]
        tips_html = "".join(
            f"<li style='margin-bottom:6px'>{tip}</li>" for tip in t["tips"]
        )
        st.markdown(f"""
        <div class='treatment-card {t["card_class"]}'>
            <b style='font-family:Sora,sans-serif;color:#e8f5e9;font-size:1rem'>
                {t["icon"]} {t["title"]}
            </b>
            <ul style='color:#c8e6c9;margin-top:10px;padding-left:18px'>
                {tips_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")

        # ── Pie chart ──
        st.markdown("#### 📊 Leaf Colour Composition")
        fig, ax = plt.subplots(figsize=(4, 4), facecolor="#0f1a10")
        ax.set_facecolor("#0f1a10")
        wedges, texts, autotexts = ax.pie(
            rgb_values, labels=["Green", "Red", "Blue"], autopct="%1.1f%%",
            colors=["#4caf50", "#ef5350", "#42a5f5"], startangle=90,
            wedgeprops={"edgecolor": "#0f1a10", "linewidth": 2}
        )
        for tx in texts:  tx.set_color("#c8e6c9"); tx.set_fontsize(11)
        for at in autotexts: at.set_color("white"); at.set_fontsize(10)
        st.pyplot(fig); plt.close(fig)

        st.write("---")

        # ── 💾 Save ──
        st.markdown("#### 💾 Save Result")
        leaf_name = st.text_input("Leaf scan name", placeholder="e.g. Field-A Sample 1")
        if st.button("💾 Save to History"):
            if leaf_name.strip() == "":
                st.warning("Please enter a name before saving.")
            else:
                st.session_state.history.append({
                    "name":       leaf_name.strip(),
                    "result":     result,
                    "confidence": confidence,
                    "condition":  condition,
                    "severity":   severity_label,
                    "timestamp":  datetime.now().strftime("%d %b %Y, %I:%M %p")
                })
                st.success(f"✅ '{leaf_name}' saved to history!")
    else:
        st.info("⬆️ Upload an image or use your camera above to scan a leaf.")

# ══════════════════════════════════════════
#  TAB 2 – ANALYTICS
# ══════════════════════════════════════════
with tab_analytics:
    st.markdown("#### 📊 Scan Analytics")

    if st.session_state.history:
        good_count = sum(1 for i in st.session_state.history if i["result"] == "GOOD")
        bad_count  = sum(1 for i in st.session_state.history if i["result"] == "BAD")
        high_risk  = sum(1 for i in st.session_state.history if "High" in i.get("severity", ""))
        total      = len(st.session_state.history)

        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='metric-box'><div class='metric-num'>{total}</div><div class='metric-label'>Total Scans</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='metric-box'><div class='metric-num' style='color:#a5d6a7'>{good_count}</div><div class='metric-label'>Healthy</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='metric-box'><div class='metric-num' style='color:#ef9a9a'>{bad_count}</div><div class='metric-label'>Diseased / Deficient</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='metric-box'><div class='metric-num' style='color:#ef5350'>{high_risk}</div><div class='metric-label'>High Risk</div></div>", unsafe_allow_html=True)

        st.write("")
        col_pie, col_bar = st.columns(2)

        with col_pie:
            st.markdown("##### Health Distribution")
            fig2, ax2 = plt.subplots(figsize=(4, 4), facecolor="#0f1a10")
            ax2.set_facecolor("#0f1a10")
            ax2.pie([good_count, bad_count], labels=["GOOD", "BAD"], autopct="%1.1f%%",
                    colors=["#4caf50", "#ef5350"], startangle=90,
                    wedgeprops={"edgecolor": "#0f1a10", "linewidth": 2})
            for tx in ax2.texts: tx.set_color("#c8e6c9")
            st.pyplot(fig2); plt.close(fig2)

        with col_bar:
            st.markdown("##### Confidence per Scan")
            names       = [i["name"][:12] for i in st.session_state.history]
            confidences = [i["confidence"] for i in st.session_state.history]
            bar_colors  = ["#4caf50" if i["result"] == "GOOD" else "#ef5350" for i in st.session_state.history]
            fig3, ax3 = plt.subplots(figsize=(5, 4), facecolor="#0f1a10")
            ax3.set_facecolor("#1a2b1c")
            ax3.bar(range(len(names)), confidences, color=bar_colors, edgecolor="#0f1a10")
            ax3.set_xticks(range(len(names)))
            ax3.set_xticklabels(names, rotation=30, ha="right", color="#c8e6c9", fontsize=9)
            ax3.set_ylabel("Confidence (%)", color="#c8e6c9", fontsize=9)
            ax3.set_ylim(0, 100); ax3.tick_params(colors="#c8e6c9")
            for spine in ax3.spines.values(): spine.set_edgecolor("#2d4a2f")
            ax3.legend(handles=[mpatches.Patch(color="#4caf50", label="GOOD"),
                                 mpatches.Patch(color="#ef5350", label="BAD")],
                       facecolor="#1a2b1c", labelcolor="white", edgecolor="#2d4a2f")
            st.pyplot(fig3); plt.close(fig3)

        # Severity breakdown bar
        st.write("")
        st.markdown("##### 🌡️ Severity Breakdown")
        sev_counts = {
            "Low Risk":    sum(1 for i in st.session_state.history if "Low"    in i.get("severity", "")),
            "Medium Risk": sum(1 for i in st.session_state.history if "Medium" in i.get("severity", "")),
            "High Risk":   sum(1 for i in st.session_state.history if "High"   in i.get("severity", "")),
        }
        fig4, ax4 = plt.subplots(figsize=(5, 2.5), facecolor="#0f1a10")
        ax4.set_facecolor("#1a2b1c")
        bars = ax4.barh(list(sev_counts.keys()), list(sev_counts.values()),
                        color=["#4caf50", "#ffa726", "#ef5350"], edgecolor="#0f1a10", height=0.5)
        ax4.set_xlabel("Count", color="#c8e6c9", fontsize=9)
        ax4.tick_params(colors="#c8e6c9")
        for spine in ax4.spines.values(): spine.set_edgecolor("#2d4a2f")
        for bar, val in zip(bars, sev_counts.values()):
            ax4.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                     str(val), va="center", color="white", fontsize=10)
        st.pyplot(fig4); plt.close(fig4)

    else:
        st.info("No scan data yet. Upload and save leaf images from the Dashboard tab.")

# ══════════════════════════════════════════
#  TAB 3 – HISTORY
# ══════════════════════════════════════════
with tab_history:
    st.markdown("#### 📁 Scan History")

    if st.session_state.history:
        if st.button("🗑️ Clear All History"):
            st.session_state.history = []
            st.rerun()

        for idx, item in enumerate(reversed(st.session_state.history), 1):
            badge     = "badge-good" if item["result"] == "GOOD" else "badge-bad"
            icon      = "✅" if item["result"] == "GOOD" else "⚠️"
            sev       = item.get("severity", "")
            ts        = item.get("timestamp", "—")
            sev_class = "sev-low" if "Low" in sev else ("sev-medium" if "Medium" in sev else "sev-high")
            t_data    = TREATMENTS.get(item["condition"], TREATMENTS["Healthy Leaf"])
            tips_html = "".join(
                f"<li style='margin-bottom:4px;color:#a5c9a7;font-size:0.82rem'>{tip}</li>"
                for tip in t_data["tips"]
            )

            st.markdown(f"""
            <div class='agro-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px'>
                    <b style='font-size:1rem;font-family:Sora,sans-serif;color:#e8f5e9'>
                        #{idx} — {item['name']}
                    </b>
                    <span class='ts-tag'>🕐 {ts}</span>
                </div>
                <br>
                <span class='{badge}'>{icon} {item['result']}</span>
                &nbsp;<span class='{sev_class}'>{sev}</span>
                &nbsp;&nbsp;
                <span style='color:#a5c9a7'>Condition: {item['condition']}</span><br>
                <span style='color:#81c784;font-size:0.85rem'>Confidence: {item['confidence']}%</span>
                <br><br>
                <details>
                    <summary style='color:#81c784;cursor:pointer;font-size:0.85rem;
                                    font-family:Sora,sans-serif;font-weight:600'>
                        💡 View Treatment Tips
                    </summary>
                    <ul style='padding-left:16px;margin-top:8px'>{tips_html}</ul>
                </details>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No history yet. Save scans from the Dashboard tab.")

# ══════════════════════════════════════════
#  TAB 4 – ABOUT
# ══════════════════════════════════════════
with tab_about:
    st.markdown("#### ℹ️ About AgroVision AI")
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""
        <div class='agro-card'>
            <h4 style='margin-top:0;color:#a5d6a7'>🌿 What It Does</h4>
            AgroVision AI analyses leaf images using colour-ratio intelligence to instantly
            detect plant health. Upload a photo or use your camera for an instant GOOD / BAD
            classification, severity rating, treatment tips, and full timestamped history.
        </div>
        <div class='agro-card'>
            <h4 style='margin-top:0;color:#a5d6a7'>🚀 Features</h4>
            • Leaf health detection (Healthy / Disease / Deficiency)<br>
            • 🌡️ Severity meter — Low / Medium / High Risk<br>
            • 📷 Camera capture or file upload<br>
            • 💡 Treatment suggestions per condition<br>
            • 📅 Timestamped scan history<br>
            • Analytics with severity breakdown chart
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='agro-card'>
            <h4 style='margin-top:0;color:#a5d6a7'>🔬 How It Works</h4>
            The model extracts average RGB values from the image and computes colour ratios.
            High green → Healthy. High red → Disease. Otherwise → Nutrient Deficiency.
            Severity is determined by result type and confidence level.
        </div>
        <div class='agro-card'>
            <h4 style='margin-top:0;color:#a5d6a7'>🔮 Future Scope</h4>
            • Deep Learning model (CNN / Vision Transformer)<br>
            • Multi-class disease classification (30+ types)<br>
            • Weather & soil data integration<br>
            • Mobile app (Android / iOS)<br>
            • Geo-tagged field reports & crop mapping
        </div>
        """, unsafe_allow_html=True)
