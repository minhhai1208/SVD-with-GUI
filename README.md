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

## 🧠 How It Works (Mathematical Explanation)

Singular Value Decomposition (SVD) is a linear algebra technique that factorizes a matrix \(A\) (here, the image) into three matrices:

$$
A = U \Sigma V^T
$$

Where:

- $A \in \mathbb{R}^{m \times n}$ is the original grayscale image matrix, with pixel intensities as entries.
- $U \in \mathbb{R}^{m \times m}$ contains the left singular vectors (orthonormal columns).
- $\Sigma \in \mathbb{R}^{m \times n}$ is a diagonal matrix of singular values 
  $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r \ge 0$, representing the "energy" or importance of each component.
- $V^T \in \mathbb{R}^{n \times n}$ contains the right singular vectors (orthonormal rows).

---

### 1️⃣ Rank-based Reconstruction

To reduce memory while preserving the most important information, we **truncate the SVD** to the top \(k\) singular values:

$$
A_k = U_k \Sigma_k V_k^T
$$

Where:

- \(U_k \in \mathbb{R}^{m \times k}\), \(\Sigma_k \in \mathbb{R}^{k \times k}\), \(V_k^T \in \mathbb{R}^{k \times n}\)
- \(k \ll \min(m, n)\), reducing storage from \(m \cdot n\) to \(k \cdot (m + n + 1)\)
- The reconstructed matrix \(A_k\) is a **low-rank approximation** that preserves the most visually significant features.

**Memory saving:**  
Instead of storing all \(m \cdot n\) pixels, we now only store:

$$
k \cdot m + k \cdot n + k = k(m+n+1)
$$

This is much smaller than the original image size if \(k\) is small.

---

### 2️⃣ Error-based Reconstruction

Alternatively, we can choose a **target percentage of information retained**. The "energy" of the image is defined as the sum of squared singular values:

$$
\text{Total Energy} = \sum_{i=1}^{r} \sigma_i^2
$$

To preserve a given percentage \(p\%\) of the image's information:

1. Compute cumulative energy:

$$
E_k = \sum_{i=1}^{k} \sigma_i^2
$$

2. Find the smallest \(k\) such that:

$$
E_k \ge \frac{p}{100} \cdot \text{Total Energy}
$$

3. Reconstruct the image using the top \(k\) singular values:

$$
A_k = U_k \Sigma_k V_k^T
$$

This ensures that the reconstructed image **retains most of the visual content** while discarding less important details (small singular values).

---

### 3️⃣ Why it Works

- Large singular values capture the **main structures, edges, and textures** of the image.
- Truncating small singular values removes **noise and fine details**, reducing memory usage.
- Low-rank approximation gives a **compressed representation**, preserving visual information with significantly fewer numbers stored.



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
