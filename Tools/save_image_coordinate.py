from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
import json
import xml.etree.ElementTree as ET
import os, sys


# Function to let the user select a rectangular frame
def on_mouse_click(event):
    global x_start, y_start, rect_id
    x_start, y_start = event.x, event.y
    rect_id = canvas.create_rectangle(
        x_start, y_start, x_start, y_start, outline="red", width=2
    )


def on_mouse_drag(event):
    global x_start, y_start, rect_id
    x_end, y_end = event.x, event.y
    canvas.coords(rect_id, x_start, y_start, x_end, y_end)


def on_mouse_release(event):
    global x_start, y_start, rect_id, x_min, y_min, x_max, y_max
    x_min, y_min = min(x_start, event.x), min(y_start, event.y)
    x_max, y_max = max(x_start, event.x), max(y_start, event.y)
    root.quit()


def display_image(image_path, root):
    global canvas, image, photo
    # Load the image
    image = Image.open(image_path)

    # Create a Tkinter window
    root = tk.Toplevel()
    root.title("Select Frame")

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the resized dimensions to fit the screen
    aspect_ratio = image.width / image.height
    if image.width > screen_width or image.height > screen_height:
        if screen_width / screen_height < aspect_ratio:
            new_width = screen_width
            new_height = int(screen_width / aspect_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * aspect_ratio)
    else:
        # Image fits within the screen, no resizing needed
        new_width, new_height = image.width, image.height

    # Resize the image
    image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a canvas to display the image
    canvas = tk.Canvas(
        root,
        width=new_width,
        height=new_height
    )
    canvas.pack()

    # Convert the image to a format Tkinter can use
    photo = ImageTk.PhotoImage(image_resized)

    # Display the image in the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)


def save_image_with_coordinates(
    directory, file_name, image, x_min, y_min, x_max, y_max
):
    draw = ImageDraw.Draw(image)
    text = f"Xmin: {x_min}, Ymin: {y_min}, Xmax: {x_max}, Ymax: {y_max}"
    font = (
        ImageFont.load_default()
    )  # You can replace this with a .ttf font if available
    draw.rectangle(
        [x_min, y_min, x_max, y_max],
        outline="red",
        width=3
    )
    draw.text(
        (x_min, y_min - 10),
        text,
        fill="red",
        font=font
    )
    png_filename = os.path.join(directory, f"{file_name}_coordinates.png")
    image.save(png_filename)
    print(f"Coordinates saved: {text}")


def save_coordinates_as_json(directory, file_name, coordinates):
    json_filename = os.path.join(directory, f"{file_name}.json")
    with open(json_filename, "w") as json_file:
        json.dump(coordinates, json_file, indent=4)
    print(f"Coordinates saved to {json_filename}")


def save_coordinates_as_xml(directory, file_name, coordinates):
    xml_filename = os.path.join(directory, f"{file_name}.xml")
    root = ET.Element("Coordinates")
    ET.SubElement(root, "Xmin").text = str(coordinates["Xmin"])
    ET.SubElement(root, "Ymin").text = str(coordinates["Ymin"])
    ET.SubElement(root, "Xmax").text = str(coordinates["Xmax"])
    ET.SubElement(root, "Ymax").text = str(coordinates["Ymax"])
    tree = ET.ElementTree(root)
    with open(xml_filename, "wb") as xml_file:
        tree.write(xml_file)
    print(f"Coordinates saved to {xml_filename}")


while True:
    # Select an image
    file_path = None
    
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )

    # Check if the dialog was cancelled
    if not file_path:
        print("No file selected. Exiting program.")
        sys.exit()  # End the program

    display_image(file_path, root)

    x_start = y_start = x_min = y_min = x_max = y_max = 0
    rect_id = None

    canvas.bind("<Button-1>", on_mouse_click)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()

    # Write and save coordinates
    if x_min != x_max and y_min != y_max:
        # Image file path (replace with your file selection logic)
        image_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract the base name without extension
        # Define the directory for saving files
        output_dir = "new_data"
        os.makedirs(
            output_dir, exist_ok=True
        )  # Create the directory if it doesn't exist

        save_image_with_coordinates(
            output_dir, image_name, image, x_min, y_min, x_max, y_max
        )

        # Coordinates
        coordinates = {
            "Xmin": x_min,
            "Ymin": y_min,
            "Xmax": x_max,
            "Ymax": y_max
        }

        save_coordinates_as_json(output_dir, image_name, coordinates)

        save_coordinates_as_xml(output_dir, image_name, coordinates)

    root.destroy()
