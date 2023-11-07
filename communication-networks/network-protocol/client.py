import socket
from Status import Status
import tkinter as tk

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_ip = "localhost"
server_port = 10000
client_socket.connect((server_ip, server_port))

# probably turn client and server into classes

def send_message(recipient_username, message):
    params = {
        "TO": recipient_username,
        "MESSAGE": message
    }

    message = format_message("POST", params)
    client_socket.send(message.encode())


    # check if shit worked


# passing username to connect and disconnect is dumb
def connect(username):
    params = {
        "USERNAME": username
    }

    message = format_message("CONNECT", params)
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()

    if response != Status.SUCCESS.value:
        print("Did not connect to server")
        exit(response)
    else:
        print("Successfully connected to server")


def disconnect(username):
    params = {
        "USERNAME": username
    }

    message = format_message("DISCONNECT", params)
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()

    if response != Status.SUCCESS.value:
        # dunno what to do
        pass

    print("Successfully disconnected from server")
    client_socket.close()


def format_message(kind, params):
    message = kind + '\n'

    for key, value in params.items():
        message += f"{key}:{value}\n"

    # remove last new line
    return message[:-1]


connect("sam")
disconnect("sam")
