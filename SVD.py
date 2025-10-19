from tkinter import *
from tkinter import filedialog as fdl, messagebox
from skimage import img_as_ubyte
from PIL import Image, ImageTk
import numpy as np
import imageio

# =========================================================
# SVD Functions
# =========================================================
def svd_rank(rank, img):
    """Reconstruct image using top 'rank' singular values."""
    A = np.array(img, dtype=float)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    A_approx = np.dot(U[:, :rank], np.dot(np.diag(S[:rank]), Vt[:rank, :]))
    return A_approx

def svd_error(percent, img):
    """Reconstruct image retaining given percentage of energy."""
    A = np.array(img, dtype=float)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    total_energy = np.sum(S**2)
    target_energy = total_energy * (percent / 100)

    energy = 0
    k = 0
    while energy < target_energy and k < len(S):
        energy += S[k]**2
        k += 1

    A_approx = np.dot(U[:, :k], np.dot(np.diag(S[:k]), Vt[:k, :]))
    return A_approx

# =========================================================
# GUI Setup
# =========================================================
root = Tk()
root.title('SVD Image Compression')
root.state('zoomed')
root.configure(background='black')

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
frame_width = screen_width / 2 - 100
frame_height = screen_height - 60
button_size = int(frame_width / 3)

# Frames
left_frame = Frame(root, bg='gray')
left_frame.place(height=frame_height, width=frame_width, x=25, y=20)

right_frame = Frame(root, bg='white')
right_frame.place(height=frame_height, width=frame_width, x=screen_width - (frame_width + 25), y=20)

option_frame = Frame(root, height=250, width=150, bg='black')
option_frame.pack(side=BOTTOM, pady=10)

# =========================================================
# Image Handling
# =========================================================
image_list = []
current_index = -1
l_photo = r_photo = None

def resize_image(img, fw, fh):
    """Resize image to fit frame."""
    w, h = img.width, img.height
    if (h / w) > (fh / fw):
        w_resize = int(fh * (w / h))
        h_resize = int(fh)
    else:
        h_resize = int(fw * (h / w))
        w_resize = int(fw)
    return img.resize((w_resize, h_resize))

def upload_left_image():
    """Upload an image and display on left frame."""
    global l_photo, left_image

    filetypes = [('Image Files', '*.jpg *.jpeg *.png *.bmp')]
    filename = fdl.askopenfilename(title='Open Image', filetypes=filetypes)
    if not filename:
        return

    left_image = Image.open(filename).convert('L')
    resized = resize_image(left_image, frame_width, frame_height)
    l_photo = ImageTk.PhotoImage(resized)

    for widget in left_frame.winfo_children():
        widget.destroy()

    Button(left_frame, image=l_photo, command=lambda: zoom_image(resized)).pack(expand=True)
    print(f"Loaded: {filename}")

def show_right_image(img):
    """Display reconstructed image."""
    global r_photo
    resized = resize_image(img, frame_width, frame_height)
    r_photo = ImageTk.PhotoImage(resized)

    for widget in right_frame.winfo_children():
        widget.destroy()

    Button(right_frame, image=r_photo, command=lambda: zoom_image(resized)).pack(expand=True)

# =========================================================
# SVD and Save Operations
# =========================================================
def process_image():
    """Apply SVD reconstruction."""
    global current_index

    if l_photo is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    try:
        value = int(textbox.get())
        mode = mode_var.get()

        if value <= 0:
            raise ValueError("Value must be positive.")

        if mode == "RANK":
            app_matrix = svd_rank(value, left_image)
        elif mode == "ERROR":
            if not (0 < value <= 100):
                raise ValueError("Error must be between 1 and 100%.")
            app_matrix = svd_error(value, left_image)
        else:
            messagebox.showerror("Error", "Invalid mode selected.")
            return

        app_image = Image.fromarray(app_matrix)
        image_list.append(app_image)
        current_index = len(image_list) - 1
        show_right_image(app_image)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def save_image():
    """Save the latest reconstructed image."""
    if current_index < 0:
        messagebox.showerror("Error", "No reconstructed image to save.")
        return

    filepath = fdl.asksaveasfilename(
        defaultextension=".jpeg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("GIF", "*.gif")],
        title="Save Image As"
    )
    if not filepath:
        return

    imageio.imwrite(filepath, np.array(image_list[current_index]))
    messagebox.showinfo("Saved", f"Image saved to {filepath}")

# =========================================================
# Zoom Feature
# =========================================================
zoom_frame = None

def zoom_image(img):
    """Open zoom view for image."""
    global zoom_frame
    zoom_frame = Frame(root, bg='#252525')
    zoom_frame.place(height=screen_height, width=screen_width)
    resized = resize_image(img, screen_width - 40, screen_height - 150)
    zm_photo = ImageTk.PhotoImage(resized)
    Button(zoom_frame, image=zm_photo, command=zoom_frame.destroy).pack(pady=40)
    zoom_frame.image = zm_photo  # prevent garbage collection

# =========================================================
# UI Elements
# =========================================================
Button(left_frame, text="Upload Image", command=upload_left_image, bg="#cccccc").place(relx=0.5, rely=0.5, anchor=CENTER)
Button(right_frame, text="Result", bg="#eeeeee").pack(pady=int(screen_height / 3))

mode_var = StringVar(value="RANK")
OptionMenu(option_frame, mode_var, "RANK", "ERROR").pack(pady=5)

textbox = Entry(option_frame, width=20)
textbox.pack(pady=5)

Button(option_frame, text="Submit", command=process_image, width=12, bg="lightgreen").pack(pady=5)
Button(option_frame, text="Save", command=save_image, width=12, bg="lightblue").pack(pady=5)

# =========================================================
root.mainloop()
