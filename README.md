# 🖼️ SVD Image Compression GUI

## 📘 Overview
This project demonstrates how **Singular Value Decomposition (SVD)** — a fundamental concept in **Linear Algebra** — can be applied to **image compression**.  
It features an **interactive GUI built with Tkinter**, allowing users to:
- Upload any grayscale image
- Choose between **rank-based** or **error-based** reconstruction
- Visualize how image quality changes as compression increases  

Through this tool, users can intuitively understand how **low-rank approximation** reduces data size while preserving visual information.

---

## ⚙️ Features
✅ **Upload and preview** any image (JPG, PNG, etc.)  
✅ **Two modes of reconstruction:**
   - **Rank-based**: Keep the top *k* singular values  
   - **Error-based**: Keep enough singular values to retain a chosen % of image energy  
✅ **Real-time visualization** of original and reconstructed images  
✅ **Zoom** to inspect details of compressed images  
✅ **Save** the reconstructed image to disk  

---

## 🧠 How It Works
The SVD of a grayscale image matrix \( A \) is given by:
\[
A = U \Sigma V^T
\]

Where:
- \( U \): left singular vectors  
- \( \Sigma \): diagonal matrix of singular values (energy)  
- \( V^T \): right singular vectors  

To approximate the image with a reduced rank \( k \):
\[
A_k = U_k \Sigma_k V_k^T
\]

This effectively **compresses** the image while preserving the most important visual features.

---

## 🖥️ GUI Overview

| Function | Description |
|-----------|--------------|
| **Upload** | Select an image from your device |
| **Mode** | Choose “RANK” or “ERROR” from dropdown |
| **Input box** | Enter rank (e.g. `50`) or error % (e.g. `90`) |
| **Submit** | Generate and display reconstructed image |
| **Save** | Save the output as JPEG or PNG |
| **Zoom** | Click image to zoom in/out |

---

## 🧩 Tech Stack

| Library | Purpose |
|----------|----------|
| **Tkinter** | GUI framework |
| **Pillow (PIL)** | Image manipulation |
| **NumPy** | Linear algebra (SVD computation) |
| **scikit-image** | Safe image type conversion |
| **imageio** | Image saving |

---

## 🚀 Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/svd-image-compression-gui.git
cd svd-image-compression-gui
