# streamlit_app.py
# ------------------------------------------------------------
# Streamlit Image Processing Demo (Pro-grade, optimized)
# Methods: Linear Negative, Contrast Stretching, Piecewise Linear,
#          Log, Gamma, Histogram Equalization, AHE, CLAHE
# Supports grayscale & color. Adjustable parameters per method.
# Shows before/after images + their histograms (per-channel for color).
# ------------------------------------------------------------
# Requirements:
#   pip install streamlit opencv-python-headless scikit-image matplotlib numpy
#
# Run:
#   streamlit run streamlit_app.py
# ------------------------------------------------------------

import io
import cv2
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from skimage import exposure, img_as_float, img_as_ubyte

st.set_page_config(page_title="Image Processing Playground", layout="wide")

# -----------------------------
# Utils
# -----------------------------
def is_grayscale(img: np.ndarray) -> bool:
    return (img.ndim == 2) or (img.ndim == 3 and img.shape[2] == 1)

def to_gray(img: np.ndarray) -> np.ndarray:
    if is_grayscale(img):
        g = img.squeeze()
        return g
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def to_bgr(img: np.ndarray) -> np.ndarray:
    if is_grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # already BGR
    return img

def read_image(file_bytes: bytes, mode: str) -> np.ndarray:
    """mode: 'auto', 'grayscale', 'color' (color in BGR)."""
    file_arr = np.frombuffer(file_bytes, dtype=np.uint8)
    if mode == "grayscale":
        img = cv2.imdecode(file_arr, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imdecode(file_arr, cv2.IMREAD_COLOR)  # BGR
        if mode == "auto" and img is None:  # fallback
            img = cv2.imdecode(file_arr, cv2.IMREAD_GRAYSCALE)
    return img

def clip01(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)

def ensure_uint8(img: np.ndarray) -> np.ndarray:
    if img.dtype == np.uint8:
        return img
    img = np.nan_to_num(img)
    if img.max() <= 1.0 + 1e-9:
        return img_as_ubyte(clip01(img))
    # assume 0-255
    return np.clip(img, 0, 255).astype(np.uint8)

def compute_hist(img: np.ndarray, bins: int = 256):
    """Return (counts, bin_edges) per channel. Grayscale returns one tuple."""
    if is_grayscale(img):
        hist, edges = np.histogram(img.flatten(), bins=bins, range=(0, 255))
        return [(hist, edges)]
    # color: BGR channels
    hists = []
    for c in range(3):
        hist, edges = np.histogram(img[:, :, c].flatten(), bins=bins, range=(0, 255))
        hists.append((hist, edges))
    return hists

def plot_histograms(img: np.ndarray, title: str):
    """Matplotlib figure of histograms (grayscale or BGR channels)."""
    fig = plt.figure(figsize=(5, 3), dpi=120)
    if is_grayscale(img):
        (hist, edges) = compute_hist(img)[0]
        plt.plot(edges[:-1], hist)
        plt.title(f"{title} Histogram")
        plt.xlabel("Intensity")
        plt.ylabel("Count")
        plt.xlim(0, 255)
        plt.tight_layout()
        return fig

    # color (B, G, R) – use default colors to comply with 'no specific colors' rule
    labels = ["B", "G", "R"]
    hists = compute_hist(img)
    for (h, e), lab in zip(hists, labels):
        plt.plot(e[:-1], h, label=lab)
    plt.title(f"{title} Histograms (Channels)")
    plt.xlabel("Intensity")
    plt.ylabel("Count")
    plt.xlim(0, 255)
    plt.legend()
    plt.tight_layout()
    return fig

# -----------------------------
# Methods (each returns uint8 image, grayscale keeps 2D)
# -----------------------------
def linear_negative(img: np.ndarray) -> np.ndarray:
    return 255 - img

def contrast_stretch(img: np.ndarray, in_low: float, in_high: float, out_low: float, out_high: float) -> np.ndarray:
    """
    in_* and out_* in [0,1]
    """
    imgf = img_as_float(img)
    stretched = exposure.rescale_intensity(imgf, in_range=(in_low, in_high), out_range=(out_low, out_high))
    return ensure_uint8(stretched)

def piecewise_linear(img: np.ndarray, x1: float, y1: float, x2: float, y2: float) -> np.ndarray:
    """
    Points are in [0,1], with mapping:
      (0,0) -> ... -> (x1,y1) -> (x2,y2) -> (1,1)
    Enforced monotonic x: 0 <= x1 <= x2 <= 1
    """
    imgf = img_as_float(img)
    x1, x2 = sorted([np.clip(x1, 0, 1), np.clip(x2, 0, 1)])
    y1, y2 = np.clip(y1, 0, 1), np.clip(y2, 0, 1)

    def pw_map(v):
        # Segment 1: [0, x1]
        s1 = (y1 - 0.0) / (x1 - 0.0 + 1e-12)
        # Segment 2: [x1, x2]
        s2 = (y2 - y1) / (x2 - x1 + 1e-12)
        # Segment 3: [x2, 1]
        s3 = (1.0 - y2) / (1.0 - x2 + 1e-12)

        out = np.empty_like(v)
        mask1 = v <= x1
        mask2 = (v > x1) & (v <= x2)
        mask3 = v > x2

        out[mask1] = s1 * (v[mask1] - 0.0) + 0.0
        out[mask2] = s2 * (v[mask2] - x1) + y1
        out[mask3] = s3 * (v[mask3] - x2) + y2
        return clip01(out)

    if is_grayscale(img):
        out = pw_map(imgf)
    else:
        out = np.dstack([pw_map(imgf[:, :, c]) for c in range(3)])
    return ensure_uint8(out)

def log_transform(img: np.ndarray, gain: float = 1.0) -> np.ndarray:
    """
    s = c * log(1 + r), r in [0,1], c = gain / log(2) so max ~ gain
    """
    imgf = img_as_float(img)
    c = gain / np.log(2.0)
    out = c * np.log1p(imgf)
    out = out / (out.max() + 1e-12)  # normalize to [0,1]
    return ensure_uint8(out)

def gamma_transform(img: np.ndarray, gamma: float = 1.0, gain: float = 1.0) -> np.ndarray:
    """
    s = gain * r^gamma; renormalize to [0,1]
    """
    imgf = img_as_float(img)
    out = gain * np.power(imgf, gamma)
    out = out / (out.max() + 1e-12)
    return ensure_uint8(out)

def hist_equalize(img: np.ndarray) -> np.ndarray:
    if is_grayscale(img):
        return cv2.equalizeHist(img)
    # color: equalize luminance only
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

def adaptive_hist_equalize(img: np.ndarray, clip_limit: float = 0.01, nbins: int = 256) -> np.ndarray:
    """
    skimage exposure.equalize_adapthist (AHE/CLAHE hybrid with clip)
    clip_limit ~ 0.01..0.05
    """
    if is_grayscale(img):
        out = exposure.equalize_adapthist(img_as_float(img), clip_limit=clip_limit, nbins=nbins)
        return ensure_uint8(out)
    # color: apply on luminance in LAB for perceptual stability
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = lab[:, :, 0] / 255.0
    L_eq = exposure.equalize_adapthist(L, clip_limit=clip_limit, nbins=nbins)
    lab[:, :, 0] = ensure_uint8(L_eq)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def clahe_opencv(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: int = 8) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(tile_grid_size, tile_grid_size))
    if is_grayscale(img):
        return clahe.apply(img)
    # color: apply to luminance in LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# -----------------------------
# Caching
# -----------------------------
@st.cache_resource(show_spinner=False)
def get_title_mark():
    return "🧮 Image Processing Playground"

@st.cache_data(show_spinner=False)
def process_image(method_key: str, img: np.ndarray, params: dict) -> np.ndarray:
    # Dispatch with pure, deterministic transforms
    if method_key == "Linear Negative":
        return linear_negative(img)
    elif method_key == "Contrast Stretching":
        return contrast_stretch(
            img,
            params.get("in_low", 0.0),
            params.get("in_high", 1.0),
            params.get("out_low", 0.0),
            params.get("out_high", 1.0),
        )
    elif method_key == "Piecewise Linear":
        return piecewise_linear(
            img,
            params.get("x1", 0.25),
            params.get("y1", 0.10),
            params.get("x2", 0.75),
            params.get("y2", 0.90),
        )
    elif method_key == "Log Transform":
        return log_transform(img, params.get("gain", 1.0))
    elif method_key == "Gamma Transform":
        return gamma_transform(img, params.get("gamma", 1.0), params.get("gain", 1.0))
    elif method_key == "Histogram Equalization":
        return hist_equalize(img)
    elif method_key == "Adaptive Hist Eq (AHE)":
        return adaptive_hist_equalize(img, params.get("clip_limit", 0.01), params.get("nbins", 256))
    elif method_key == "CLAHE (OpenCV)":
        return clahe_opencv(img, params.get("clip_limit", 2.0), params.get("tile_grid_size", 8))
    else:
        return img

# -----------------------------
# Sidebar Controls
# -----------------------------
st.title(get_title_mark())
st.caption("Professional demo: choose a method, tune parameters, and compare before/after with histograms. Works for grayscale or color.")

with st.sidebar:
    st.header("⚙️ Controls")
    img_mode = st.radio("Image type to upload", options=["Auto", "Grayscale", "Color"], index=0, help="Auto tries color first; grayscale if needed.")
    method = st.selectbox(
        "Processing Method",
        options=[
            "Linear Negative",
            "Contrast Stretching",
            "Piecewise Linear",
            "Log Transform",
            "Gamma Transform",
            "Histogram Equalization",
            "Adaptive Hist Eq (AHE)",
            "CLAHE (OpenCV)",
        ],
        index=4,
    )
    st.divider()
    # Dynamic params per method
    params = {}
    if method == "Contrast Stretching":
        st.markdown("**Input Range (in_range)** in [0,1]")
        in_low, in_high = st.slider("in_low / in_high", 0.0, 1.0, (0.02, 0.98), 0.01)
        st.markdown("**Output Range (out_range)** in [0,1]")
        out_low, out_high = st.slider("out_low / out_high", 0.0, 1.0, (0.0, 1.0), 0.01)
        params.update({"in_low": in_low, "in_high": in_high, "out_low": out_low, "out_high": out_high})
    elif method == "Piecewise Linear":
        st.markdown("**Breakpoints & Mapped Values** (all in [0,1])")
        x1 = st.slider("x1", 0.0, 1.0, 0.25, 0.01)
        y1 = st.slider("y1", 0.0, 1.0, 0.10, 0.01)
        x2 = st.slider("x2", 0.0, 1.0, 0.75, 0.01)
        y2 = st.slider("y2", 0.0, 1.0, 0.90, 0.01)
        params.update({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
    elif method == "Log Transform":
        gain = st.slider("gain", 0.1, 5.0, 1.0, 0.1)
        params.update({"gain": gain})
    elif method == "Gamma Transform":
        gamma = st.slider("gamma (γ)", 0.05, 5.0, 1.2, 0.05)
        gain = st.slider("gain", 0.1, 5.0, 1.0, 0.1)
        params.update({"gamma": gamma, "gain": gain})
    elif method == "Adaptive Hist Eq (AHE)":
        clip = st.slider("clip_limit (0.005–0.1 typical)", 0.001, 0.2, 0.01, 0.001)
        nbins = st.slider("nbins", 32, 512, 256, 16)
        params.update({"clip_limit": clip, "nbins": int(nbins)})
    elif method == "CLAHE (OpenCV)":
        clip = st.slider("clipLimit", 0.1, 10.0, 2.0, 0.1)
        tiles = st.slider("tileGridSize (tiles per side)", 2, 32, 8, 1)
        params.update({"clip_limit": clip, "tile_grid_size": int(tiles)})

    st.divider()
    st.markdown("**Display Options**")
    show_channel_hists = st.checkbox("Show per-channel histograms for color", value=True)
    equalize_on_luma_info = st.checkbox("Equalize on luminance for color (recommended)", value=True, help="This app already uses luminance for color equalization methods.")

    st.caption("Tip: For color images, histograms show each channel. For equalization, luminance (Y/L) is used to maintain colors.")

# -----------------------------
# Main Area
# -----------------------------
up = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
if up is None:
    st.info("Upload a sample image to begin. Color photos show best contrast differences; grayscale also supported.")
    st.stop()

# Read image
user_mode = img_mode.lower()
if user_mode == "auto":
    src_img = read_image(up.read(), "auto")
elif user_mode == "grayscale":
    src_img = read_image(up.read(), "grayscale")
else:
    src_img = read_image(up.read(), "color")

if src_img is None:
    st.error("Failed to read the image. Please try a different file.")
    st.stop()

# Normalize input type
src_img = ensure_uint8(src_img)

# Process
dst_img = process_image(method, src_img, params)
dst_img = ensure_uint8(dst_img)

# -----------------------------
# Layout: Before/After
# -----------------------------
c1, c2 = st.columns(2, vertical_alignment="top")
with c1:
    st.subheader("Before")
    st.image(to_bgr(src_img), channels="BGR", use_column_width=True, caption="Original")
    fig1 = plot_histograms(src_img if show_channel_hists else to_gray(src_img), "Before")
    st.pyplot(fig1, clear_figure=True)
with c2:
    st.subheader("After")
    st.image(to_bgr(dst_img), channels="BGR", use_column_width=True, caption=f"{method}")
    fig2 = plot_histograms(dst_img if show_channel_hists else to_gray(dst_img), "After")
    st.pyplot(fig2, clear_figure=True)

# -----------------------------
# Download
# -----------------------------
st.divider()
bcol1, bcol2, bcol3 = st.columns([1,1,2])
with bcol1:
    # Encode for download
    ok, buf = cv2.imencode(".png", to_bgr(dst_img))
    if ok:
        st.download_button(
            label="⬇️ Download Processed Image (PNG)",
            data=buf.tobytes(),
            file_name=f"processed_{method.replace(' ','_').lower()}.png",
            mime="image/png",
        )
with bcol2:
    st.write(f"**Mode:** {'Grayscale' if is_grayscale(src_img) else 'Color'}")
    st.write(f"**Size:** {src_img.shape[1]} × {src_img.shape[0]}")

# -----------------------------
# Notes & Best Practices
# -----------------------------
with st.expander("Notes / Implementation Details"):
    st.markdown(
        """
- **Color handling:** Histogram Equalization / AHE / CLAHE operate on luminance (Y in YCrCb or L in LAB) to preserve color fidelity.
- **Scaling:** Many transforms run on normalized float [0,1] then converted back to uint8.
- **Piecewise Linear:** Two breakpoints `(x1,y1)`, `(x2,y2)` split the curve into three linear segments.
- **Performance:** Stateless transforms are cached via `@st.cache_data`. Heavy resources can be cached via `@st.cache_resource`.
- **Security:** Processing is fully in-memory; no server-side persistence of user images.
        """
    )
