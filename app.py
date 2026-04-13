import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="☕ Drink Detector",
    page_icon="☕",
    layout="centered",
)

# ─── Pastel Theme ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* ── Base ── */
html, body, .stApp {
    background: #fdf6f0;
    font-family: 'Nunito', sans-serif;
    color: #3d2e2e;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.4rem 0 0.6rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #f9a8c9 0%, #fde68a 50%, #bbf0b2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 2px 8px #f9a8c930);
}
.hero-sub {
    color: #b08a8a;
    font-size: 1rem;
    font-weight: 600;
}

/* ── Class pills ── */
.pill-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin: 1rem 0 1.4rem; justify-content: center; }
.pill {
    display: flex; align-items: center; gap: 0.4rem;
    padding: 0.4rem 1.1rem; border-radius: 999px;
    font-size: 0.83rem; font-weight: 800; border: 2px solid;
    letter-spacing: 0.02em;
}
.pill-coffee { background: #fff0f6; border-color: #f9a8c9; color: #c2607a; }
.pill-black  { background: #fffbeb; border-color: #fde68a; color: #92720a; }
.pill-matcha { background: #f0fff4; border-color: #bbf0b2; color: #3a7d44; }

/* ── Section label ── */
.card-title {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #f9a8c9;
    margin-bottom: 0.55rem;
}

/* ── Metric boxes ── */
.metrics-row { display: flex; gap: 0.7rem; margin: 0.8rem 0; }
.metric-box {
    flex: 1;
    background: #fff8fb;
    border: 2px solid #f9a8c940;
    border-radius: 16px;
    padding: 0.9rem 0.5rem;
    text-align: center;
    box-shadow: 0 2px 12px #f9a8c915;
}
.metric-val { font-size: 1.8rem; font-weight: 900; }
.metric-lbl { font-size: 0.65rem; color: #b08a8a; margin-top: 0.15rem; letter-spacing: 0.06em; text-transform: uppercase; font-weight: 700; }
.mv-coffee { color: #f472a8; }
.mv-black  { color: #d4a800; }
.mv-matcha { color: #52b96a; }
.mv-total  { color: #a78bfa; }

/* ── Detection list ── */
.det-row { display: flex; flex-direction: column; gap: 0.5rem; }
.det-item {
    display: flex; align-items: center; justify-content: space-between;
    background: #fff8fb;
    border: 2px solid #f9a8c930;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    box-shadow: 0 1px 6px #f9a8c910;
}
.det-label { font-weight: 800; font-size: 0.92rem; }
.det-conf { font-size: 0.78rem; font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 8px; }
.conf-high { background: #d1fae5; color: #059669; }
.conf-mid  { background: #fef3c7; color: #b45309; }
.conf-low  { background: #ffe4e6; color: #e11d48; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 2.5rem;
    background: #fff8fb;
    border: 2px dashed #f9a8c960;
    border-radius: 20px;
    color: #c08a9a;
    font-weight: 600;
    font-size: 0.95rem;
}

/* ── Steps ── */
.step { display: flex; align-items: flex-start; gap: 0.85rem; margin-bottom: 0.6rem; }
.step-num {
    background: linear-gradient(135deg, #f9a8c9, #bbf0b2);
    color: #3d2e2e;
    border-radius: 50%;
    width: 26px; height: 26px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 0.75rem;
    flex-shrink: 0; margin-top: 2px;
}
.step-text { color: #7a5c5c; font-size: 0.88rem; line-height: 1.6; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #fff0f6 !important;
    border-right: 2px solid #f9a8c940 !important;
}
section[data-testid="stSidebar"] * { color: #3d2e2e !important; }
section[data-testid="stSidebar"] .stMarkdown code { background: #ffe4f0 !important; }

/* ── Slider accent ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #f9a8c9 !important;
    border-color: #f9a8c9 !important;
}

/* ── Buttons ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #f9a8c9 0%, #fde68a 100%);
    color: #3d2e2e;
    font-weight: 900;
    font-size: 1rem;
    border: none;
    border-radius: 14px;
    padding: 0.72rem;
    cursor: pointer;
    transition: opacity .18s, transform .18s;
    box-shadow: 0 4px 16px #f9a8c940;
    letter-spacing: 0.02em;
}
div.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #bbf0b2 0%, #fde68a 100%) !important;
    color: #3d2e2e !important;
    font-weight: 900 !important;
    border: none !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px #bbf0b230 !important;
}

/* ── Radio / file uploader ── */
div[data-testid="stFileUploader"] {
    background: #fff8fb;
    border: 2px dashed #f9a8c960;
    border-radius: 14px;
    padding: 0.5rem;
}
.stRadio label { font-weight: 700 !important; }

/* ── Info / success / warning ── */
.stAlert { border-radius: 14px !important; font-weight: 600; }

/* ── Divider ── */
hr { border-color: #f9a8c930 !important; }

/* ── Camera input ── */
div[data-testid="stCameraInput"] button {
    background: linear-gradient(135deg, #f9a8c9, #fde68a) !important;
    color: #3d2e2e !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    border: none !important;
}

/* ── Expander ── */
details { background: #fff8fb; border: 2px solid #f9a8c930 !important; border-radius: 14px !important; }
summary { font-weight: 800 !important; color: #c2607a !important; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
# pastel pink → coffee, pastel yellow → black coffee, pastel green → matcha
CLASS_COLORS = {
    "coffee":       "#f472a8",
    "black_coffee": "#d4a800",
    "matcha":       "#52b96a",
}
CLASS_EMOJIS = {
    "coffee":       "☕",
    "black_coffee": "🖤",
    "matcha":       "🍵",
}

def get_color(name: str) -> str:
    n = name.lower().replace(" ", "_")
    for k, v in CLASS_COLORS.items():
        if k in n:
            return v
    return "#a78bfa"

def get_emoji(name: str) -> str:
    n = name.lower().replace(" ", "_")
    for k, v in CLASS_EMOJIS.items():
        if k in n:
            return v
    return "🔍"

def conf_cls(c: float) -> str:
    if c >= 0.70: return "conf-high"
    if c >= 0.45: return "conf-mid"
    return "conf-low"

def metric_color(name: str) -> str:
    n = name.lower()
    if "black" in n:  return "mv-black"
    if "coffee" in n: return "mv-coffee"
    if "matcha" in n: return "mv-matcha"
    return "mv-total"

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">☕ Drink Detector</div>
  <div class="hero-sub">Take a photo of your drink and see what it is!</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pill-row">
  <div class="pill pill-coffee">☕ Coffee</div>
  <div class="pill pill-black">🖤 Black Coffee</div>
  <div class="pill pill-matcha">🍵 Matcha</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    conf_threshold = st.slider("Confidence", 0.10, 0.95, 0.35, 0.05,
                                help="Higher = only show strong detections")
    iou_threshold  = st.slider("Overlap threshold", 0.10, 0.95, 0.45, 0.05,
                                help="Controls how much boxes can overlap")

    st.markdown("---")
    st.markdown("""
<div style='font-size:0.82rem;line-height:1.9;color:#7a5c5c;font-weight:700'>
  Detectable drinks:<br>
  ☕ <span style='color:#f472a8'>Coffee</span><br>
  🖤 <span style='color:#d4a800'>Black Coffee</span><br>
  🍵 <span style='color:#52b96a'>Matcha</span>
</div>
""", unsafe_allow_html=True)

# ─── Load Model ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from ultralytics import YOLO
        model_path = os.path.join(os.path.dirname(__file__), "best.pt")
        return YOLO(model_path), None
    except ImportError:
        return None, "ultralytics not installed — pip install ultralytics"
    except Exception as e:
        return None, str(e)

model, model_error = load_model()
if model_error:
    st.error(f"❌ Could not load model: {model_error}")

# ─── Input ────────────────────────────────────────────────────────────────────
st.markdown("---")
mode = st.radio("", ["📷 Camera", "🖼️ Upload image"], horizontal=True)

image = None
if mode == "📷 Camera":
    cam = st.camera_input("Take a photo of your drink")
    if cam:
        image = Image.open(cam).convert("RGB")
else:
    up = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
    if up:
        image = Image.open(up).convert("RGB")

# ─── Detection ────────────────────────────────────────────────────────────────
if image and model:
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card-title">📸 Your Photo</div>', unsafe_allow_html=True)
        st.image(image, use_container_width=True)

    with st.spinner("Detecting…"):
        results = model.predict(
            source=np.array(image),
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False,
        )
        result = results[0]

    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    detections = []

    if result.boxes is not None and len(result.boxes):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        except:
            font = ImageFont.load_default()

        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf   = float(box.conf[0])
            name   = result.names[cls_id]
            color  = get_color(name)
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
            lw = max(3, int(min(image.size) * 0.005))

            draw.rectangle([x1, y1, x2, y2], outline=color, width=lw)
            label = f"{get_emoji(name)} {name.replace('_',' ')}  {conf:.0%}"
            try:
                tb = draw.textbbox((x1, y1 - 26), label, font=font)
                draw.rectangle([tb[0]-4, tb[1]-3, tb[2]+4, tb[3]+3], fill=color)
                draw.text((x1, y1 - 26), label, fill="#ffffff", font=font)
            except:
                draw.text((x1, max(0, y1 - 20)), label, fill=color, font=font)

            detections.append({"name": name, "conf": conf, "color": color})

    with col2:
        st.markdown('<div class="card-title">🔍 Result</div>', unsafe_allow_html=True)
        st.image(annotated, use_container_width=True)

    st.markdown("---")

    if detections:
        counts = {}
        for d in detections:
            counts[d["name"]] = counts.get(d["name"], 0) + 1

        metrics_html = '<div class="metrics-row">'
        for cls_name, cnt in counts.items():
            mc = metric_color(cls_name)
            metrics_html += f"""
            <div class="metric-box">
              <div class="metric-val {mc}">{cnt}</div>
              <div class="metric-lbl">{get_emoji(cls_name)} {cls_name.replace('_',' ')}</div>
            </div>"""
        metrics_html += f"""
            <div class="metric-box">
              <div class="metric-val mv-total">{len(detections)}</div>
              <div class="metric-lbl">🔢 Total</div>
            </div>
        </div>"""
        st.markdown(metrics_html, unsafe_allow_html=True)

        st.markdown('<div class="card-title" style="margin-top:1.1rem">📋 Detections</div>', unsafe_allow_html=True)
        det_html = '<div class="det-row">'
        for d in sorted(detections, key=lambda x: -x["conf"]):
            cc = conf_cls(d["conf"])
            det_html += f"""
            <div class="det-item">
              <span class="det-label" style="color:{d['color']}">
                {get_emoji(d['name'])} {d['name'].replace('_',' ')}
              </span>
              <span class="det-conf {cc}">{d['conf']:.1%}</span>
            </div>"""
        det_html += "</div>"
        st.markdown(det_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        buf = io.BytesIO()
        annotated.save(buf, format="PNG")
        st.download_button(
            "⬇️ Save Result",
            data=buf.getvalue(),
            file_name="drink_detection.png",
            mime="image/png",
        )

    else:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.8rem; margin-bottom:0.6rem">🔍</div>
          No drinks detected.<br>
          <span style="font-size:0.85rem;color:#c08a9a">Try moving closer or adjusting the confidence slider.</span>
        </div>""", unsafe_allow_html=True)



# ─── How it Works ─────────────────────────────────────────────────────────────
with st.expander("✨ How it works"):
    st.markdown("""
<div class="step"><div class="step-num">1</div><div class="step-text">
Take a photo using your camera or upload one from your gallery.
</div></div>
<div class="step"><div class="step-num">2</div><div class="step-text">
The AI model scans the image and draws a box around each drink it finds.
</div></div>
<div class="step"><div class="step-num">3</div><div class="step-text">
Each detection shows the drink type and a confidence score (how sure the model is).
</div></div>
<div class="step"><div class="step-num">4</div><div class="step-text">
Save the annotated image using the <b>Save Result</b> button.
</div></div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:#e8c8d8;font-size:0.75rem;padding:2.5rem 0 0.5rem;font-weight:700'>
  ☕ Drink Detector · Powered by YOLOv8
</div>
""", unsafe_allow_html=True)
