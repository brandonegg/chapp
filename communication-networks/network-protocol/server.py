from Status import Status
import socket
import threading
from Log import Log
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log = Log()


server_socket.bind(("0.0.0.0", 10000))

server_socket.listen()
log.info("Server is listening for incoming connections...")

# username => client socket
clients = {}

# username => (username => ("message": <message>, "time": <timestamp>))
messages = {}


def parse_response(data):
    lines = data.split('\n')
    request_type = lines[0]

    params = {}

    for line in lines[1:]:
        key, value = line.split(':', 1)
        params[key.strip()] = value.strip()

    return request_type, params


def handle_client(client, address):
    while True:
        try:
            data = client.recv(1024).decode()
            request_type, params = parse_response(data)

            # case 1: connecting
            # type : CONNECT
            # params : USERNAME
            if request_type == "CONNECT":
                clients[params['USERNAME']] = client
                client.send(Status.SUCCESS.value.encode())

                log.info(f"User: {params['USERNAME']} {address} successfully connected")

            # case 2: disconencting
            # type : DISCONNECT
            # params : USERNAME
            if request_type == "DISCONNECT":
                del clients[params['USERNAME']]
                client.send(Status.SUCCESS.value.encode())

                log.info(f"User: {params['USERNAME']} {address} successfully disconnected")
                return

            # case 3: sending message
            # type : POST
            # params: TO, MESSAGE
            if request_type == "POST":
                timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
                message = params['MESSAGE']

                recipient_client = params['TO']


        except:
            continue


while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
