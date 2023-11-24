
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import client
import select
import threading
import time
import json
import ast



def dm(chat_client: client.ChatClient, to_user: str):

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame1")

    # Filter messages involving the specified username
    filtered_messages = [msg for msg in chat_client.messages if msg['from_user'] == to_user or msg['to_user'] == to_user]
    sorted_messages = sorted(filtered_messages, key=lambda x: x['timestamp'])


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Tk()

    window.geometry("1920x1080")
    window.configure(bg = "#FFFFFF")

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
    # bg rectangle
    canvas.create_rectangle(
        483.0,
        129.0,
        1437.0,
        952.0,
        fill="#332222",
        outline="")

    canvas.create_text(
        909.0,
        179.0,
        anchor="nw",
        text="DM\n",
        fill="#FFFFFF",
        font=("Inter", 60 * -1)
    )

    y_offset = 300  # Initial Y offset for displaying messages
    # Iterate over the last 20 messages (or less if there are fewer than 20 messages)
    # until i get pages working, or never teehee
    for message in sorted_messages[-20:]:
        text = f"{message['timestamp']} - {message['from_user']}: {message['message']}"
        canvas.create_text(
            600,
            y_offset,
            anchor="nw",
            text=text,
            fill="#FFFFFF",
            font=("Inter", 14)
        )
        y_offset += 30  # Increment Y offset to display next message

    # Function to refresh the display with updated messages
    def refresh_display():
        canvas.delete("all")  # Clear the canvas

        filtered_messages = [msg for msg in chat_client.messages if msg['from_user'] == to_user or msg['to_user'] == to_user]
        sorted_messages = sorted(filtered_messages, key=lambda x: x['timestamp'])
        canvas.place(x = 0, y = 0)
        # bg rectangle
        canvas.create_rectangle(
            483.0,
            129.0,
            1437.0,
            952.0,
            fill="#332222",
            outline="")

        canvas.create_text(
            909.0,
            179.0,
            anchor="nw",
            text="DM\n",
            fill="#FFFFFF",
            font=("Inter", 60 * -1)
        )

        y_offset = 300  # Initial Y offset for displaying messages
        for message in sorted_messages[-20:]:
            text = f"{message['timestamp']} - {message['from_user']}: {message['message']}"
            canvas.create_text(
                600,
                y_offset,
                anchor="nw",
                text=text,
                fill="#FFFFFF",
                font=("Inter", 14)
            )
            y_offset += 30  # Increment Y offset for the next message

    # Function to send the message when the button is clicked
    def send_message():
        message_text = message_entry.get()  # Get the text from the Entry widget
        if message_text == "":
            return
        # Clear the Entry widget after sending the message
        message_entry.delete(0, 'end')
        # Code to send the message using chat_client
        
        response = chat_client.post(to_user, message_text)

        if response.fields["status"] == 100:
            chat_client.messages.append(ast.literal_eval(response.fields["message"]))


    # Create an Entry widget for typing the message
    message_entry = Entry(window, font=("Inter", 12))
    message_entry.place(x=600, y=900)

    # Create a Button to send the message
    send_button = Button(window, text="Send", command=send_message)
    send_button.place(x=900, y=900)

    def refresh_loop():
        while True:
            refresh_display()
            time.sleep(1)

    listening_thread = threading.Thread(target=refresh_loop, args=())
    listening_thread.start()


    window.resizable(False, False)
    window.mainloop()
