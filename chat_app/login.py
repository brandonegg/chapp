
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import client
import json

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, StringVar


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1920x1080")
window.configure(bg = "#FFFFFF")

def draw_rounded_rectangle(canvas, x, y, width, height, radius, color):
    canvas.create_rectangle(
        x + radius,
        y,
        x + width - radius,
        y + height,
        fill=color,
        outline=color
    )
    canvas.create_rectangle(
        x,
        y + radius,
        x + width,
        y + height - radius,
        fill=color,
        outline=color
    )
    canvas.create_oval(
        x,
        y,
        x + 2 * radius,
        y + 2 * radius,
        fill=color,
        outline=color
    )
    canvas.create_oval(
        x + width - 2 * radius,
        y,
        x + width,
        y + 2 * radius,
        fill=color,
        outline=color
    )
    canvas.create_oval(
        x,
        y + height - 2 * radius,
        x + 2 * radius,
        y + height,
        fill=color,
        outline=color
    )
    canvas.create_oval(
        x + width - 2 * radius,
        y + height - 2 * radius,
        x + width,
        y + height,
        fill=color,
        outline=color
    )

def draw_circle(canvas, x, y, diameter, color):
    canvas.create_oval(x, y, x + diameter, y + diameter, fill=color, outline="")

def draw_circle_from_rectangle(canvas, x1, y1, x2, y2, color):
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    radius = min(x2 - x1, y2 - y1) / 2
    canvas.create_oval(x_center - radius, y_center - radius, x_center + radius, y_center + radius, fill=color, outline="")

def login_pressed():
    username = entry_username.get()  # Get username from Entry field
    print(username)
    # Call login function from client.py
    chat_client = client.ChatClient(username)
    chat_client.connect_to("127.0.0.1", 6969)
    response = chat_client.introduce()
    response_success = response.fields["status"] == 100 

    if response_success:
        print(response)
        data_string = response.fields["messages"]
        start_index = data_string.find("[")
        end_index = data_string.rfind("]") + 1
        messages_str = data_string[start_index:end_index]
        messages_str = messages_str.replace("'", '"')
        messages = json.loads(messages_str)
        window.destroy()
        import dms
        dms.dms(chat_client, messages, username)
    else:
        # Handle failed login (e.g., show an error message)
        print("Login failed, status code:", response.fields["status"])
        # make a label that says username logged in already
        window.after(100, show_error_message)  # Schedule error message after a delay

def show_error_message():
    error_label.place(x=615, y=250)  # Fixed position for error label
    error_label.config(text="Login failed. Please try again.", fg="red", font=("Arial", 30))  # Update error label

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
# background rectangle
canvas.create_rectangle(
    483.0,
    129.0,
    1437.0,
    952.0,
    fill="#332222",
    outline="")

# login rectangle
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    964.5,
    446.5,
    image=entry_image_1
)
entry_username = Entry(
    bd=0,
    bg="#800909",
    fg="#000716",
    highlightthickness=0
)
entry_username.place(
    x=671.5,
    y=402.0,
    width=586.0,
    height=87.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: login_pressed(),
    relief="flat"
)
button_2.place(
    x=763.0,
    y=643.0,
    width=394.0,
    height=82.0
)

error_label = Label(window, text="", fg="red")  # Label to show error message
# circle pfp background
draw_circle_from_rectangle(canvas, 561.0, 380.0, 693.0, 512.0, "#D9D9D9")

#head
draw_circle_from_rectangle(canvas, 604.0, 400.0, 650.0, 446.0, "#999999")

#body
x1, y1 = 588.0, 444.0
x2, y2 = 667.0, 532.0

canvas.create_arc(
    x1, y1, x2, y2,
    start=357, extent=186,
    fill="#999999", outline=""
)

canvas.create_text(
    880.0,
    181.0,
    anchor="nw",
    text="Login",
    fill="#FFFFFF",
    font=("Inter", 60 * -1)
)
window.resizable(False, False)
window.mainloop()
