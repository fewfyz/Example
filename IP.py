Anfield
anfield_d
👀 กำลังจับผีเสื้อไอ้ควาย…
รวบรวมสิ่งที่เรียนในวิชา coding

Sheeperino

 — 25/8/68 17:04
@Anfield
ภาพ
ภาพ
Anfield — 25/8/68 17:08
dframe2 = pd.DataFrame([[1,2,3,np.nan],[2,np.nan,5,6],[np.nan,7,np.nan,9],[1,np.nan,np.nan,np.nan]])
dframe3 = dframe2.fillna({'0' : dframe2[0].mean()})
Sheeperino

 — 25/8/68 17:08
Filling missing numerical values with the median of the column
df_filled_median = df.fillna({'col1': df['col1'].median()})
print("\nDataFrame after fillna() with median for 'col1':")
display(df_filled_median)

Filling missing categorical values with the mode of the column
 For mode, if there are multiple modes, it returns a Series, so we take the first one [0]
df_filled_mode = df.fillna({'col2': df['col2'].mode()[0]})
print("\nDataFrame after fillna() with mode for 'col2':")
display(df_filled_mode)

Forward fill
df_filled_ffill = df.fillna(method='ffill')
print("\nDataFrame after forward fill (method='ffill'):")
display(df_filled_ffill)

Backward fill
df_filled_bfill = df.fillna(method='bfill')
print("\nDataFrame after backward fill (method='bfill'):")
display(df_filled_bfill) 
Anfield — 25/8/68 17:17
dframe2 = pd.DataFrame([[1,2,3,np.nan],[2,np.nan,5,6],[np.nan,7,np.nan,9],[1,np.nan,np.nan,np.nan]])
df3 = dframe2.apply(lambda col: col.fillna(col.mean()) if col.name in [0,1,2,3] else col)
Sheeperino

 — 25/8/68 17:22
ภาพ
Sheeperino

 — 25/8/68 17:37
import numpy as np

data = np.array([10, 12, 12, 13, 12, 11, 200, 13, 12, 11])

mean = np.mean(data)   # ≈ 30.6
std = np.std(data)     # ≈ 56.1

z_scores = (data - mean) / std
print(z_scores.round(2))
-----------------------------
import numpy as np

data = np.array([10, 12, 12, 13, 12, 11, 200, 13, 12, 11])

mean = np.mean(data)
std = np.std(data)

z_scores = (data - mean) / std
outliers = data[np.abs(z_scores) > 3]

print("Outliers:", outliers)
Sheeperino

 — 25/8/68 17:47
-------------

Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]
print("Outliers:", outliers)
-------------------------------
Forward fill
df_filled_ffill = df.fillna(method='ffill')
print("\nDataFrame after forward fill (method='ffill'):")
display(df_filled_ffill)

Backward fill
df_filled_bfill = df.fillna(method='bfill')
print("\nDataFrame after backward fill (method='bfill'):")
display(df_filled_bfill) 
===================================
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [24, 30, 18],
    "city": ["NY", "LA", "Paris"]
})

print(df)
------------------------------------------------------
Sheeperino

 — 25/8/68 17:55
df.iloc[0]   # first row
Sheeperino

 — 25/8/68 18:02
🧩 1. None
Python built-in.
Means “nothing here” or “no value assigned.”
It’s literally a Python object: type(None) is NoneType.
Usually used in normal Python code (not just data stuff).

x = None
print(x is None)  # True


---

🧩 2. NaN (Not a Number)
Comes from NumPy / math.
Special float value: float('nan').
Used in data science to mark missing or invalid numeric values.
Weird quirk: np.nan != np.nan (it doesn’t equal itself).

import numpy as np
x = np.nan
print(x == np.nan)  # False
print(np.isnan(x))  # True ✅ correct way


---

🧩 3. NULL
SQL/database concept.
Means “no entry in this column.”
In pandas, when you load SQL data, NULL values usually become NaN (for numbers) or None (for objects/strings).

SELECT * FROM users WHERE email IS NULL;


---

🧠 Quick Comparison
| Value  | Origin      | Meaning                           | Example                        |
| ------ | ----------- | --------------------------------- | ------------------------------ |
| None | Python core | Absence of value (general)        | missing arg in a function      |
| NaN  | NumPy/float | Missing/invalid numeric value | bad sensor reading, empty cell |
| NULL | Databases   | No value in DB field              | empty SQL column               |

---

🔄 How they mix in pandas
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "a": [1, None, 3],
    "b": [4, np.nan, 6]
})

print(df)


Output:

     a    b
0  1.0  4.0
1  NaN  NaN   <- notice None got converted to NaN
2  3.0  6.0


So pandas often just unifies everything → NaN.

---

⚡️ TL;DR:

None → Python’s “nothing.”
NaN → Numeric “missing value” (float).
Null → Database “nothing.”
In pandas: everything basically becomes NaN.
Juniormnn — 25/8/68 18:05
1. Padas Dataframe DATAseries missingvalue ML(supersvised, unsupervided) plot (writing) validation (Training set, testing set)
2. Coding (Project) : provide data (dataprep) select ML yourself #Recheck Accuracy 
	Regression


ขยาย
อจ บอกข้อสอบ.txt
1 KB
Sheeperino

 — 25/8/68 18:06
what if pd.Series([1,np.nan,2,None])
ภาพ
Jarb — 25/8/68 18:08
ตอนแรกก็ไม่เครียดนะ พอเริ่มเห็น Code ในดิสเริ่มเครียดละ
Juniormnn — 25/8/68 18:10
มาได้น้า เจอร์ ว่าง
Jarb — 25/8/68 18:11
ทำงานค้าบ เดี๋ยวส่องเอาจากในดิส
Juniormnn — 25/8/68 18:12
กำลังคุยเรื่อง clean data กันเฉยๆ พวก outlier กับ Nan
Sheeperino

 — 25/8/68 18:24
@Juniormnn @Anfield
Sheeperino

 — 25/8/68 18:44
@Juniormnn @Anfield
Sheeperino

 — 25/8/68 20:16
🔎 What it does
drop_duplicates() removes duplicate rows from a DataFrame (or duplicate values from a Series).

By default, it keeps the first occurrence and drops the rest.
You can control which columns matter for “duplicate checking.”

---

⚡️ Example
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
    "age": [25, 30, 25, 35, 30],
    "city": ["NY", "LA", "NY", "Paris", "LA"]
})

print("Original:")
print(df)

print("\nDrop duplicates:")
print(df.drop_duplicates())


Output
Original:
      name  age   city
0    Alice   25     NY
1      Bob   30     LA
2    Alice   25     NY
3  Charlie   35  Paris
4      Bob   30     LA

Drop duplicates:
      name  age   city
0    Alice   25     NY
1      Bob   30     LA
3  Charlie   35  Paris


---

🎯 Options
subset
Pick specific columns to check for duplicates:

df.drop_duplicates(subset=["name"])


👉 drops rows where "name" repeats.

---

keep
Choose which duplicate to keep:

"first" (default) → keep first occurrence.
"last" → keep last occurrence.
False → drop all duplicates.

df.drop_duplicates(keep="last")


---

inplace
Do the operation directly on the DataFrame:

df.drop_duplicates(inplace=True)


---

📝 Quick Summary
No args → removes full row duplicates.
subset → removes based on specific columns.
keep → controls which duplicate is kept.
inplace → changes the DataFrame directly.
🐍 Example 2: Series duplicates
s = pd.Series([1, 2, 2, 3, 3, 3, 4])

print("Original Series:")
print(s, "\n")

print("drop_duplicates (default):")
print(s.drop_duplicates(), "\n")

print("drop_duplicates keep='last':")
print(s.drop_duplicates(keep="last"), "\n")

print("drop_duplicates keep=False:")
print(s.drop_duplicates(keep=False))


---

🖨 Output
Original Series:
0    1
1    2
2    2
3    3
4    3
5    3
6    4

drop_duplicates (default):
0    1
1    2
3    3
6    4

drop_duplicates keep='last':
0    1
2    2
5    3
6    4

drop_duplicates keep=False:
0    1
6    4


---

✨ TL;DR:

DataFrame → removes duplicate rows (or by subset of cols).
Series → removes duplicate values.
keep decides whether first, last, or none of the duplicates survive.
Sheeperino

 — 25/8/68 20:24
print("drop_duplicates on 'name':")
print(df.drop_duplicates(subset=["name"]), "\n")
-----------------------------------

กันตาย Machine learning
🚀 Easiest “just run it” ML script (classification)
# filename: quick_ml.py
# deps: scikit-learn (pip install scikit-learn), numpy

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1) Load toy data (Iris)
data = load_iris()
X, y = data.data, data.target
target_names = data.target_names

# 2) Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3) Model — Random Forest (no scaling needed)
model = RandomForestClassifier(
    n_estimators=200, random_state=42
)
model.fit(X_train, y_train)

# 4) Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\n📊 Classification report:")
print(classification_report(y_test, y_pred, target_names=target_names))

# 5) Try a quick prediction
sample = X_test[0:1]
pred_idx = model.predict(sample)[0]
print("\n🔮 Sample prediction:", target_names[pred_idx])

# 6) Save the model
joblib.dump(model, "iris_rf_model.joblib")
print("\n💾 Saved model to iris_rf_model.joblib")


🧰 How to run
pip install scikit-learn joblib
python quick_ml.py


---

🧪 Variations (swap-in one line if you want)
Logistic Regression (needs scaling but fine on Iris):

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000, random_state=42)


Support Vector Machine:

from sklearn.svm import SVC
model = SVC(kernel="rbf", probability=True, random_state=42)
Sheeperino

 — 25/8/68 20:33
กันตาย missing value
---

🧰 Pandas fillna() Cheat Sheet
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "A": [1, 2, np.nan, 4],
    "B": [np.nan, 5, 6, np.nan],
    "C": ["x", None, "y", None]
})

print("Original:")
print(df, "\n")


---

1️⃣ Fill with a constant
df.fillna(0)   # replace all NaNs with 0


---

2️⃣ Fill with column mean/median/mode
df["A"].fillna(df["A"].mean(), inplace=True)     # mean
df["B"].fillna(df["B"].median(), inplace=True)   # median
df["C"].fillna(df["C"].mode()[0], inplace=True)  # most common value


---

3️⃣ Fill forward / backward (propagate values)
df.fillna(method="ffill")   # forward-fill (copy value from above)
df.fillna(method="bfill")   # backward-fill (copy value from below)


---

4️⃣ Fill different values for each column
df.fillna({"A": 0, "B": 99, "C": "missing"})


---

5️⃣ Fill only a limited number of NaNs
df.fillna(method="ffill", limit=1)


👉 fills only the first NaN it encounters per column.

---

6️⃣ Fill in-place
df.fillna(0, inplace=True)


👉 modifies the DataFrame directly (doesn’t return a copy).

---

7️⃣ Interpolation (fancy fill)
df["A"].interpolate(method="linear", inplace=True)   # line between neighbors


---

8️⃣ Fill row-wise (instead of per column)
df.apply(lambda row: row.fillna(row.mean()), axis=1)


👉 fills each row’s NaN with that row’s mean.

---

📝 Quick Summary
Constant value → df.fillna(0)
Statistical value → df.fillna(df.mean())
Method → "ffill", "bfill"
Custom per column → dict
Limit how many → limit
Row-wise → apply(..., axis=1)
Interpolation → .interpolate()

---
Juniormnn — 26/8/68 14:34
@Juniormnn @Opelly
Sheeperino

 — 26/8/68 20:38
🐍 Matplotlib Cheat Sheet
import matplotlib.pyplot as plt
import numpy as np

# toy data
x = np.linspace(0, 10, 100)
y = np.sin(x)


---

🎯 Basic Plot
plt.plot(x, y)                 # line plot
plt.title("Basic Plot")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()


---

🎯 Scatter Plot
plt.scatter(x, y, color="red", marker="o")
plt.title("Scatter")
plt.show()


---

🎯 Bar Plot
categories = ["A", "B", "C"]
values = [10, 30, 20]

plt.bar(categories, values, color="skyblue")
plt.title("Bar Chart")
plt.show()
---

🎯 Horizontal Bar
plt.barh(categories, values, color="orange")
plt.title("Horizontal Bar")
plt.show()


---

🎯 Histogram
data = np.random.randn(1000)

plt.hist(data, bins=30, color="purple", alpha=0.7)
plt.title("Histogram")
plt.show()


---

🎯 Pie Chart
sizes = [15, 30, 45, 10]
labels = ["Cats", "Dogs", "Birds", "Fish"]

plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("Pie Chart")
plt.show()


---

🎯 Multiple Lines
plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)")
plt.legend()
plt.title("Multiple Lines")
plt.show()


---

🎯 Subplots (grid of plots)
fig, axs = plt.subplots(2, 2, figsize=(8, 6))

axs[0,0].plot(x, np.sin(x))
axs[0,1].plot(x, np.cos(x))
axs[1,0].hist(data, bins=20)
axs[1,1].scatter(x, y)

plt.tight_layout()
plt.show()


---

🎯 Styling & Extras
plt.plot(x, y, linestyle="--", color="green", marker="o", label="sin")
plt.grid(True)
plt.legend()
plt.show()


---

📝 Quick Reference
plt.plot() → line plot
plt.scatter() → scatter plot
plt.bar() / plt.barh() → bar chart
plt.hist() → histogram
plt.pie() → pie chart
plt.subplot() / plt.subplots() → multiple plots
plt.title(), plt.xlabel(), plt.ylabel() → labels
plt.legend() → legend
plt.grid(True) → add grid

---

⚡ pro-tip: you can change the whole style with one line:

plt.style.use("seaborn-v0_8")  # or 'ggplot', 'classic', 'dark_background'


---
Quick Reference

plt.plot() → line plot

plt.scatter() → scatter plot

plt.bar() / plt.barh() → bar chart

plt.hist() → histogram

plt.pie() → pie chart

plt.subplot() / plt.subplots() → multiple plots

plt.title(), plt.xlabel(), plt.ylabel() → labels

plt.legend() → legend

plt.grid(True) → add grid
Sheeperino

 — 26/8/68 21:16
ประเภทไฟล์ที่แนบ: archive
archive.zip
2.24 KB
Sheeperino

 — 26/8/68 21:50
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดplyplotโนหนึ่ง.ipynb
144.23 KB
Sheeperino

 — 26/8/68 22:35
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดML_unsoup.ipynb
66.16 KB
Sheeperino

 — 26/8/68 23:33
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดML_soup.ipynb
63.27 KB
ภาพ
ภาพ
Jarb — 27/8/68 11:13
ประเภทไฟล์ที่แนบ: acrobat
UntMidterm.pdf
1.42 MB
Sheeperino

 — 27/8/68 13:17
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

# numeric features
X = df[["calories","protein","fat","sugars","fiber","carbo","rating"]]

# Standardize
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)

# PCA to 2 components
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot
plt.scatter(X_pca[:,0], X_pca[:,1], c=df["type"].map({"C":0, "H":1}), cmap="coolwarm", alpha=0.7)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA of Cereals")
plt.show()
Sheeperino

 — 29/8/68 20:47
@plan 3
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดML_soup.ipynb
63.27 KB
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดML_unsoup(1).ipynb
66.16 KB
ประเภทไฟล์ที่แนบ: unknown
ตริ้วโหดplyplotโนหนึ่ง.ipynb
144.23 KB
Sheeperino

 — 16/9/68 11:32
import pandas as pd
import seaborn as sns

# Load the Iris dataset from seaborn
df = sns.load_dataset("iris")  # columns: sepal_length, sepal_width, petal_length, petal_width, species
cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
data = df[cols]

# Compute stats
mean_vals = data.mean(numeric_only=True)
median_vals = data.median(numeric_only=True)
mode_vals = data.mode(numeric_only=True).iloc[0]   # take first mode if multiple

# Build summary table (Mean / Mode / Median)
summary = pd.DataFrame({
    "Sepal length": [mean_vals["sepal_length"], mode_vals["sepal_length"], median_vals["sepal_length"]],
    "Sepal width":  [mean_vals["sepal_width"],  mode_vals["sepal_width"],  median_vals["sepal_width"]],
    "Petal length": [mean_vals["petal_length"], mode_vals["petal_length"], median_vals["petal_length"]],
    "Petal width":  [mean_vals["petal_width"],  mode_vals["petal_width"],  median_vals["petal_width"]],
}, index=["Mean", "Mode", "Median"]).round(3)

print(summary)

# Optional: save
summary.to_csv("iris_mean_mode_median.csv", index=True)
 
ภาพ
Sheeperino

 — 16/9/68 13:22
Histogram นับความถี่
Auo.in — 13:40
streamlit>=1.36.0
numpy>=1.23.0
pillow>=10.0.0
matplotlib>=3.7.0
scikit-image>=0.22.0
requirements.txt
# app.py
# Streamlit Image Processing Playground (professional & optimized)
# Run: streamlit run app.py

import io
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

from skimage import exposure, img_as_float
from skimage.color import rgb2hsv, hsv2rgb, rgb2ycbcr, ycbcr2rgb, rgb2gray

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Image Processing Lab",
    page_icon="🎛️",
    layout="wide"
)

# -----------------------------
# Helper utilities
# -----------------------------
def to_float01(arr):
    """Ensure array is float32 in [0,1]."""
    a = np.asarray(arr)
    if a.dtype.kind in ("u", "i"):
        # assume 8-bit if max > 1
        a = a.astype(np.float32)
        if a.max() > 1.0:
            a /= 255.0
    else:
        a = a.astype(np.float32)
    # clip just in case
    return np.clip(a, 0.0, 1.0)

def pil_to_nd(arr_pil, force_gray=False):
    """PIL -> np.float32 [0,1], grayscale or color."""
    if force_gray:
        if arr_pil.mode != "L":
            arr_pil = arr_pil.convert("L")
        a = to_float01(np.array(arr_pil))  # (H, W)
    else:
        if arr_pil.mode in ("L", "I;16", "I", "F"):
            # keep grayscale
            a = to_float01(np.array(arr_pil))
        else:
            arr_pil = arr_pil.convert("RGB")
            a = to_float01(np.array(arr_pil))  # (H, W, 3)
    return a

def nd_to_pil(a):
    """np [0,1] -> PIL uint8."""
    a = np.clip(a, 0.0, 1.0)
    if a.ndim == 2:
        return Image.fromarray((a * 255).astype(np.uint8), mode="L")
    elif a.ndim == 3 and a.shape[2] == 3:
        return Image.fromarray((a * 255).astype(np.uint8), mode="RGB")
    else:
        raise ValueError("Unsupported image shape for PIL conversion.")

def plot_histogram(image, is_color: bool, title: str):
    """Return a matplotlib figure with histogram(s)."""
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=150)
    if is_color:
        # per-channel hist (RGB)
        for i, label in enumerate(["R", "G", "B"]):
            ch = image[..., i].ravel()
            ax.hist(ch, bins=256, range=(0, 1), histtype="step", linewidth=1.5, label=label)
        ax.legend()
    else:
        ax.hist(image.ravel(), bins=256, range=(0, 1), histtype="stepfilled", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Intensity (0–1)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig

def piecewise_linear_transform(img, x1, y1, x2, y2):
    """
    Piecewise linear with 3 segments:
    (0,0)->(x1,y1)->(x2,y2)->(1,1).
    Vectorized via np.interp on flattened array.
    """
    x_points = np.array([0.0, x1, x2, 1.0], dtype=np.float32)
    y_points = np.array([0.0, y1, y2, 1.0], dtype=np.float32)
    x_points = np.clip(x_points, 0, 1)
    y_points = np.clip(y_points, 0, 1)
    # enforce monotonic x to avoid interp errors
    x_points = np.maximum.accumulate(x_points)
    flat = img.reshape(-1)
    out = np.interp(flat, x_points, y_points).astype(np.float32)
    return out.reshape(img.shape)

def apply_hist_equalization_color_rgb(img_rgb, method="global", clip_limit=0.01, tile_grid=(8, 8)):
    """
    Equalize luminance to avoid color shifts.
    method: "global" (HE), "ahe" (clip_limit≈1.0), "clahe" (clip_limit user)
... (241 บรรทัด)
ย่อ
message.txt
13 KB
Sheeperino

 — 13:41
สาทุ🙏
﻿
# app.py
# Streamlit Image Processing Playground (professional & optimized)
# Run: streamlit run app.py

import io
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

from skimage import exposure, img_as_float
from skimage.color import rgb2hsv, hsv2rgb, rgb2ycbcr, ycbcr2rgb, rgb2gray

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Image Processing Lab",
    page_icon="🎛️",
    layout="wide"
)

# -----------------------------
# Helper utilities
# -----------------------------
def to_float01(arr):
    """Ensure array is float32 in [0,1]."""
    a = np.asarray(arr)
    if a.dtype.kind in ("u", "i"):
        # assume 8-bit if max > 1
        a = a.astype(np.float32)
        if a.max() > 1.0:
            a /= 255.0
    else:
        a = a.astype(np.float32)
    # clip just in case
    return np.clip(a, 0.0, 1.0)

def pil_to_nd(arr_pil, force_gray=False):
    """PIL -> np.float32 [0,1], grayscale or color."""
    if force_gray:
        if arr_pil.mode != "L":
            arr_pil = arr_pil.convert("L")
        a = to_float01(np.array(arr_pil))  # (H, W)
    else:
        if arr_pil.mode in ("L", "I;16", "I", "F"):
            # keep grayscale
            a = to_float01(np.array(arr_pil))
        else:
            arr_pil = arr_pil.convert("RGB")
            a = to_float01(np.array(arr_pil))  # (H, W, 3)
    return a

def nd_to_pil(a):
    """np [0,1] -> PIL uint8."""
    a = np.clip(a, 0.0, 1.0)
    if a.ndim == 2:
        return Image.fromarray((a * 255).astype(np.uint8), mode="L")
    elif a.ndim == 3 and a.shape[2] == 3:
        return Image.fromarray((a * 255).astype(np.uint8), mode="RGB")
    else:
        raise ValueError("Unsupported image shape for PIL conversion.")

def plot_histogram(image, is_color: bool, title: str):
    """Return a matplotlib figure with histogram(s)."""
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=150)
    if is_color:
        # per-channel hist (RGB)
        for i, label in enumerate(["R", "G", "B"]):
            ch = image[..., i].ravel()
            ax.hist(ch, bins=256, range=(0, 1), histtype="step", linewidth=1.5, label=label)
        ax.legend()
    else:
        ax.hist(image.ravel(), bins=256, range=(0, 1), histtype="stepfilled", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Intensity (0–1)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig

def piecewise_linear_transform(img, x1, y1, x2, y2):
    """
    Piecewise linear with 3 segments:
    (0,0)->(x1,y1)->(x2,y2)->(1,1).
    Vectorized via np.interp on flattened array.
    """
    x_points = np.array([0.0, x1, x2, 1.0], dtype=np.float32)
    y_points = np.array([0.0, y1, y2, 1.0], dtype=np.float32)
    x_points = np.clip(x_points, 0, 1)
    y_points = np.clip(y_points, 0, 1)
    # enforce monotonic x to avoid interp errors
    x_points = np.maximum.accumulate(x_points)
    flat = img.reshape(-1)
    out = np.interp(flat, x_points, y_points).astype(np.float32)
    return out.reshape(img.shape)

def apply_hist_equalization_color_rgb(img_rgb, method="global", clip_limit=0.01, tile_grid=(8, 8)):
    """
    Equalize luminance to avoid color shifts.
    method: "global" (HE), "ahe" (clip_limit≈1.0), "clahe" (clip_limit user)
    Uses HSV V channel for global HE and Y in YCbCr for AHE/CLAHE via skimage.adapthist.
    """
    if method == "global":
        hsv = rgb2hsv(img_rgb)
        v = hsv[..., 2]
        v_eq = exposure.equalize_hist(v)
        hsv[..., 2] = np.clip(v_eq, 0, 1)
        return hsv2rgb(hsv)

    # For adaptive methods, using Y (luma) is often a bit more stable
    ycbcr = rgb2ycbcr(img_rgb)
    Y = ycbcr[..., 0] / 255.0  # skimage returns Y in [0,255] float

    if method == "ahe":
        # AHE approximated by equalize_adapthist with clip_limit ~ 1.0 (no clipping),
        # skimage requires (0,1], so we use a high value
        Y_eq = exposure.equalize_adapthist(Y, clip_limit=1.0, nbins=256, kernel_size=tile_grid)
    elif method == "clahe":
        Y_eq = exposure.equalize_adapthist(Y, clip_limit=clip_limit, nbins=256, kernel_size=tile_grid)
    else:
        raise ValueError("Unknown method for color equalization.")

    ycbcr[..., 0] = np.clip(Y_eq * 255.0, 0, 255)
    out = ycbcr2rgb(ycbcr)
    return np.clip(out, 0, 1)

# -----------------------------
# Sidebar: Inputs
# -----------------------------
st.title("🎛️ Image Processing Lab")
st.caption("Select a method, tune parameters, and compare before/after with histograms.")

with st.sidebar:
    st.header("1) Upload Image")
    uploaded = st.file_uploader("Upload an image (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])
    img_mode = st.radio("Interpret upload as:", ["Auto-detect", "Grayscale", "Color"], index=0)
    st.divider()
    st.header("2) Choose Method")
    method = st.selectbox(
        "Processing method",
        [
            "Linear Negative",
            "Contrast Stretching",
            "Piecewise Linear Transformation",
            "Log Transformation",
            "Gamma Transformation",
            "Histogram Equalization",
            "Adaptive Histogram Equalization",
            "CLAHE (Contrast Limited AHE)",
        ],
        index=0
    )

    # Per-method parameter controls
    params = {}
    if method == "Contrast Stretching":
        params["low_pct"] = st.slider("Low percentile (%)", 0.0, 10.0, 2.0, 0.1)
        params["high_pct"] = st.slider("High percentile (%)", 90.0, 100.0, 98.0, 0.1)
    elif method == "Piecewise Linear Transformation":
        st.caption("Three segments: (0,0)→(x1,y1)→(x2,y2)→(1,1)")
        params["x1"] = st.slider("x1", 0.0, 1.0, 0.25, 0.01)
        params["y1"] = st.slider("y1", 0.0, 1.0, 0.15, 0.01)
        params["x2"] = st.slider("x2", 0.0, 1.0, 0.75, 0.01)
        params["y2"] = st.slider("y2", 0.0, 1.0, 0.85, 0.01)
    elif method == "Log Transformation":
        st.caption("s = c·log(1 + r); higher c amplifies dark regions.")
        params["c"] = st.slider("c (gain)", 0.1, 5.0, 1.0, 0.1)
    elif method == "Gamma Transformation":
        st.caption("s = r^γ (γ<1 brightens, γ>1 darkens)")
        params["gamma"] = st.slider("γ (gamma)", 0.10, 5.00, 0.80, 0.01)
    elif method == "Adaptive Histogram Equalization":
        params["tile"] = st.slider("Tile grid size", 4, 32, 8, 1)
        st.caption("No clipping (pure AHE). Larger tile increases local contrast.")
    elif method == "CLAHE (Contrast Limited AHE)":
        params["tile"] = st.slider("Tile grid size", 4, 32, 8, 1)
        params["clip"] = st.slider("Clip limit", 0.005, 0.2, 0.01, 0.005)
        st.caption("Clip limit prevents over-amplification of noise.")

    st.divider()
    st.header("3) Output")
    allow_download = st.checkbox("Enable download of processed image", value=True)

# -----------------------------
# Load image
# -----------------------------
if uploaded is None:
    st.info("Upload an image to begin.")
    st.stop()

# Read with PIL
pil_image = Image.open(uploaded)
force_gray = (img_mode == "Grayscale")
force_color = (img_mode == "Color")

if force_gray:
    np_img = pil_to_nd(pil_image, force_gray=True)  # (H,W)
    is_color = False
elif force_color:
    np_img = pil_to_nd(pil_image, force_gray=False)
    if np_img.ndim == 2:
        # convert to 3-channel grayscale
        np_img = np.dstack([np_img]*3)
    is_color = True
else:
    # auto-detect
    if pil_image.mode in ("L", "I;16", "I", "F"):
        np_img = pil_to_nd(pil_image, force_gray=True)
        is_color = False
    else:
        np_img = pil_to_nd(pil_image, force_gray=False)
        if np_img.ndim == 2:
            np_img = np.dstack([np_img]*3)
            is_color = True
        else:
            is_color = (np_img.ndim == 3 and np_img.shape[2] == 3)

# -----------------------------
# Apply processing
# -----------------------------
proc = None

if method == "Linear Negative":
    # s = 1 - r
    proc = 1.0 - np_img

elif method == "Contrast Stretching":
    low = np.percentile(np_img, params.get("low_pct", 2.0))
    high = np.percentile(np_img, params.get("high_pct", 98.0))
    if is_color:
        # Rescale per channel for stability
        proc = np.empty_like(np_img)
        for c in range(3):
            c_low = np.percentile(np_img[..., c], params["low_pct"])
            c_high = np.percentile(np_img[..., c], params["high_pct"])
            proc[..., c] = exposure.rescale_intensity(np_img[..., c], in_range=(c_low, c_high), out_range=(0, 1))
    else:
        proc = exposure.rescale_intensity(np_img, in_range=(low, high), out_range=(0, 1))

elif method == "Piecewise Linear Transformation":
    x1, y1, x2, y2 = params["x1"], params["y1"], params["x2"], params["y2"]
    if is_color:
        proc = np.empty_like(np_img)
        for c in range(3):
            proc[..., c] = piecewise_linear_transform(np_img[..., c], x1, y1, x2, y2)
    else:
        proc = piecewise_linear_transform(np_img, x1, y1, x2, y2)

elif method == "Log Transformation":
    c = params["c"]
    # Normalize after log to [0,1]
    if is_color:
        proc = c * np.log1p(np_img)
        proc -= proc.min()
        proc /= (proc.max() + 1e-9)
    else:
        proc = c * np.log1p(np_img)
        proc -= proc.min()
        proc /= (proc.max() + 1e-9)

elif method == "Gamma Transformation":
    gamma = params["gamma"]
    # s = r^gamma (assuming r in [0,1])
    proc = np.power(np_img, gamma, dtype=np.float32)

elif method == "Histogram Equalization":
    if is_color:
        proc = apply_hist_equalization_color_rgb(np_img, method="global")
    else:
        proc = exposure.equalize_hist(np_img)

elif method == "Adaptive Histogram Equalization":
    # AHE via equalize_adapthist with clip_limit ~ 1.0
    tile = params["tile"]
    kernel = (tile, tile)
    if is_color:
        proc = apply_hist_equalization_color_rgb(np_img, method="ahe", tile_grid=kernel)
    else:
        proc = exposure.equalize_adapthist(np_img, kernel_size=kernel, clip_limit=1.0, nbins=256)

elif method == "CLAHE (Contrast Limited AHE)":
    tile = params["tile"]
    clip = params["clip"]
    kernel = (tile, tile)
    if is_color:
        proc = apply_hist_equalization_color_rgb(np_img, method="clahe", clip_limit=clip, tile_grid=kernel)
    else:
        proc = exposure.equalize_adapthist(np_img, kernel_size=kernel, clip_limit=clip, nbins=256)

else:
    st.error("Unknown method.")
    st.stop()

proc = np.clip(proc, 0.0, 1.0)

# -----------------------------
# Display: before / after + histograms
# -----------------------------
st.subheader("Preview")
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("**Before**")
    st.image(nd_to_pil(np_img), use_column_width=True)
    fig1 = plot_histogram(np_img if not isinstance(np_img, Image.Image) else np.array(np_img), is_color, "Histogram (Before)")
    st.pyplot(fig1, clear_figure=True)

with c2:
    st.markdown("**After — {}**".format(method))
    st.image(nd_to_pil(proc), use_column_width=True)
    fig2 = plot_histogram(proc, is_color, "Histogram (After)")
    st.pyplot(fig2, clear_figure=True)

# -----------------------------
# Download
# -----------------------------
if allow_download:
    out_pil = nd_to_pil(proc)
    buf = io.BytesIO()
    fmt = "PNG"
    out_pil.save(buf, format=fmt)
    st.download_button(
        label="Download processed image",
        data=buf.getvalue(),
        file_name=f"processed_{method.replace(' ', '_').lower()}.png",
        mime="image/png",
        type="primary"
    )

# -----------------------------
# Footer note
# -----------------------------
with st.expander("Notes & Tips"):
    st.markdown(
        """
- **Grayscale vs Color**: Histogram Equalization/AHE/CLAHE on color images works on luminance to avoid hue shifts.
- **Contrast Stretching**: Use percentiles to robustly ignore outliers.
- **Piecewise Linear**: Tune `(x1,y1)` and `(x2,y2)` to lift shadows or compress highlights.
- **Log/Gamma**: Great for bringing out details in dark or bright regions respectively.
        """
    )
message.txt
13 KB
