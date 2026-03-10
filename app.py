import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="LT-iScan",
    page_icon="🔍",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }
.block-container { padding: 2rem 3rem; }
#MainMenu, footer, header { visibility: hidden; }

.navbar {
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 0 0 1.5rem 0;
    border-bottom: 1.5px solid #f0f0f0;
    margin-bottom: 2rem;
}
.navbar-brand { display: flex; align-items: center; gap: 12px; }
.brand-icon {
    width: 42px; height: 42px; background: #1a56db;
    border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 20px;
}
.brand-name { font-size: 1.3rem; font-weight: 800; color: #111; letter-spacing: -0.5px; }
.brand-tag  { font-size: 0.7rem; color: #9ca3af; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }

.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600;
}
.status-on  { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.status-off { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-on  { background: #10b981; }
.dot-off { background: #ef4444; }

/* Tab styling */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f9fafb;
    padding: 4px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 6px 20px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: #6b7280 !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important;
    color: #1a56db !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

[data-testid="stFileUploader"] section {
    border: 2px dashed #e5e7eb !important;
    border-radius: 14px !important;
    background: #fafafa !important;
    padding: 2rem !important;
}
[data-testid="stFileUploader"] section:hover { border-color: #1a56db !important; }

/* Camera input */
[data-testid="stCameraInput"] > div {
    border: 2px dashed #e5e7eb !important;
    border-radius: 14px !important;
    background: #fafafa !important;
}
[data-testid="stCameraInput"] > div:hover { border-color: #1a56db !important; }
[data-testid="stCameraInputButton"] {
    background: #1a56db !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
}

[data-testid="stMetric"] {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 12px; padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important; font-weight: 600 !important;
    color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.8px;
}
[data-testid="stMetricValue"] {
    font-size: 2rem !important; font-weight: 800 !important; color: #111827 !important;
}

.p-card {
    background: #ffffff; border: 1.5px solid #e5e7eb;
    border-radius: 14px; padding: 22px 16px;
    text-align: center; transition: all 0.2s ease;
    position: relative; overflow: hidden;
}
.p-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #1a56db, #06b6d4);
}
.p-card:hover {
    border-color: #1a56db;
    box-shadow: 0 4px 20px rgba(26,86,219,0.1);
    transform: translateY(-2px);
}
.p-count { font-size: 2.6rem; font-weight: 800; color: #1a56db; line-height: 1; margin: 0; }
.p-label { font-size: 0.72rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 8px; }
.p-bar-wrap { background: #f3f4f6; border-radius: 99px; height: 4px; margin-top: 12px; overflow: hidden; }
.p-bar { height: 4px; border-radius: 99px; background: linear-gradient(90deg, #1a56db, #06b6d4); }

.sec-head {
    font-size: 0.7rem; font-weight: 700; color: #9ca3af;
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;
}
.img-wrap { border-radius: 14px; overflow: hidden; border: 1.5px solid #e5e7eb; }

.stButton > button[kind="primary"] {
    background: #1a56db !important; border: none !important;
    border-radius: 10px !important; padding: 0.65rem 2rem !important;
    font-weight: 700 !important; font-size: 0.9rem !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1e40af !important;
    box-shadow: 0 4px 16px rgba(26,86,219,0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px !important; overflow: hidden;
    border: 1px solid #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)


def check_api():
    try:
        return requests.get(f"{API_URL}/", timeout=3).status_code == 200
    except:
        return False


def run_detection(image: Image.Image, filename: str, filetype: str):
    """Send image to API and return parsed response."""
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    resp = requests.post(
        f"{API_URL}/lt_iscan_predict",
        files={"file": (filename, buf, filetype)},
        timeout=30
    )
    return resp


def show_results(resp):
    """Render detection results — shared by both upload & camera flows."""
    if resp.status_code == 200:
        data    = resp.json()
        summary = data.get("product_summary", [])
        total   = data.get("total_detections", 0)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Detected",  total)
        c2.metric("Unique Products", len(summary))
        c3.metric("Status", "✓ Done")

        st.write("")

        if summary:
            st.markdown('<p class="sec-head">Products Found</p>', unsafe_allow_html=True)

            n_cols    = min(len(summary), 3)
            card_cols = st.columns(n_cols)

            for idx, item in enumerate(summary):
                pct = round(item["count"] / total * 100) if total else 0
                with card_cols[idx % n_cols]:
                    st.markdown(f"""
                    <div class="p-card">
                        <p class="p-count">{item['count']}</p>
                        <p class="p-label">{item['product_name']}</p>
                        <div class="p-bar-wrap">
                            <div class="p-bar" style="width:{pct}%"></div>
                        </div>
                        <p style="font-size:0.68rem;color:#d1d5db;margin-top:6px;font-weight:600">
                            {pct}% of total
                        </p>
                    </div>""", unsafe_allow_html=True)

            st.write("")
            st.markdown('<p class="sec-head">Full Breakdown</p>', unsafe_allow_html=True)
            st.dataframe(
                {
                    "Product Name": [i["product_name"] for i in summary],
                    "Count":        [i["count"] for i in summary],
                    "Share (%)":    [f"{round(i['count']/total*100)}%" if total else "—" for i in summary],
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No products detected. Try a clearer image or different angle.")

    else:
        st.error(f"API error: {resp.json().get('error', f'HTTP {resp.status_code}')}")


# ─────────────────────────────────────────────────────────────────────────────
api_ok = check_api()

# Navbar
status_html = (
    '<span class="status-badge status-on"><span class="dot dot-on"></span>API Online</span>'
    if api_ok else
    '<span class="status-badge status-off"><span class="dot dot-off"></span>API Offline</span>'
)
st.markdown(f"""
<div class="navbar">
    <div class="navbar-brand">
        <div class="brand-icon">🔍</div>
        <div>
            <div class="brand-name">LT-iScan</div>
            <div class="brand-tag">LT-iScan Detection System</div>
        </div>
    </div>
    {status_html}
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1.1], gap="large")

with left:
    tab_upload, tab_camera = st.tabs(["📁  Upload Image", "📷  Capture Photo"])

    # ── Tab 1: Upload ─────────────────────────────────────────────────────────
    with tab_upload:
        st.write("")
        uploaded = st.file_uploader(
            "Drag & drop or click to browse",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            label_visibility="collapsed",
            key="file_upload"
        )

        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"📄 {uploaded.name}  ·  {image.width}×{image.height}px  ·  {round(uploaded.size/1024,1)} KB")
            st.write("")
            run_upload = st.button("Run Detection →", type="primary",
                                   use_container_width=True, key="btn_upload")
        else:
            st.markdown("""
            <div style="padding:3rem 1rem;text-align:center;">
                <div style="font-size:3rem">🖼️</div>
                <p style="margin-top:12px;font-size:0.85rem;color:#9ca3af">
                    No image uploaded yet
                </p>
            </div>""", unsafe_allow_html=True)
            run_upload = False

    # ── Tab 2: Camera ─────────────────────────────────────────────────────────
    with tab_camera:
        st.write("")
        st.caption("Allow camera access, then click **Take Photo** to capture and detect.")
        captured = st.camera_input("Take a photo", label_visibility="collapsed", key="camera")

        if captured:
            image_cam = Image.open(captured).convert("RGB")
            st.caption(f"📷 Captured  ·  {image_cam.width}×{image_cam.height}px")
            st.write("")
            run_camera = st.button("Run Detection →", type="primary",
                                   use_container_width=True, key="btn_camera")
        else:
            run_camera = False


# ── Results panel ─────────────────────────────────────────────────────────────
with right:
    st.markdown('<p class="sec-head">Detection Results</p>', unsafe_allow_html=True)

    # Determine active image & trigger
    has_upload = "file_upload" in st.session_state and uploaded is not None
    has_camera = "camera" in st.session_state and captured is not None

    active_run   = run_upload or run_camera
    active_image = None
    active_name  = "image.jpg"

    if run_upload and uploaded:
        active_image = image
        active_name  = uploaded.name
    elif run_camera and captured:
        active_image = image_cam
        active_name  = "capture.jpg"

    if not has_upload and not has_camera:
        st.markdown("""
        <div style="border:2px dashed #f0f0f0;border-radius:14px;
            padding:5rem 2rem;text-align:center;">
            <div style="font-size:2.5rem">📊</div>
            <p style="color:#d1d5db;font-size:0.85rem;margin-top:12px">
                Upload or capture an image to get started
            </p>
        </div>""", unsafe_allow_html=True)

    elif active_run and active_image:
        if not api_ok:
            st.error("⚠️ API is offline. Please start `main.py` on port 8000.")
        else:
            with st.spinner("Running detection…"):
                try:
                    resp = run_detection(active_image, active_name, "image/jpeg")
                    show_results(resp)
                except requests.exceptions.ConnectionError:
                    st.error("Connection refused. Make sure `main.py` is running.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    else:
        st.markdown("""
        <div style="border:2px dashed #f0f0f0;border-radius:14px;
            padding:5rem 2rem;text-align:center;">
            <div style="font-size:2.5rem">⚡</div>
            <p style="color:#d1d5db;font-size:0.85rem;margin-top:12px">
                Press <strong style="color:#1a56db">Run Detection</strong> to analyze
            </p>
        </div>""", unsafe_allow_html=True)