from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog

# Function to let the user select a rectangular frame
def on_mouse_drag(event):
    global x_start, y_start, rect_id
    x_end, y_end = event.x, event.y
    canvas.coords(rect_id, x_start, y_start, x_end, y_end)

def on_mouse_release(event):
    global x_start, y_start, rect_id, x_min, y_min, x_max, y_max
    x_min, y_min = min(x_start, event.x), min(y_start, event.y)
    x_max, y_max = max(x_start, event.x), max(y_start, event.y)
    root.quit()

def on_mouse_click(event):
    global x_start, y_start, rect_id
    x_start, y_start = event.x, event.y
    rect_id = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline="red", width=2)

# Select an image
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
image = Image.open(file_path)

# Create a tkinter window to select a frame
root = tk.Toplevel()
root.title("Select Frame")
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()
photo = tk.PhotoImage(file=file_path)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)
x_start = y_start = x_min = y_min = x_max = y_max = 0
rect_id = None

canvas.bind("<Button-1>", on_mouse_click)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

root.mainloop()

# Write and save coordinates
if x_min != x_max and y_min != y_max:
    draw = ImageDraw.Draw(image)
    text = f"Xmin: {x_min}, Ymin: {y_min}, Xmax: {x_max}, Ymax: {y_max}"
    font = ImageFont.load_default()  # You can replace this with a .ttf font if available
    draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)
    draw.text((x_min, y_min - 10), text, fill="red", font=font)
    image.save("output_with_coordinates.png")
    print(f"Coordinates saved: {text}")
