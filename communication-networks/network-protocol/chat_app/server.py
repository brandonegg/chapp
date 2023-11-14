import socket
import threading
import time
from exceptions import UnparsableRequestException
from request import ChatAppRequest

class ClientMap():
    def __init__(self):
        self.__address_socket_map = {}

    def add_client(self, socket, username):
        pass # TODO: Throw error if username already taken

class ChatServer():
    def __init__(self):
        self.socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = ClientMap()

    def listen_to(self, port: int):
        self.__bind_socket_in(port)
        self.socket_in.listen()
        self.__request_handler_loop()

    def handle_request(self, client_socket: socket.socket, client_address: str):
        try:
            request = ChatAppRequest(client_socket.recv(1024).decode())
        except UnparsableRequestException as e:
            response = ChatAppRequest()
            response.type = "RESPONSE"
            response.to_user = "unknown"
            response.from_user = "server"
            response.fields["status"] = e.status_code

            print(response)
        print(request)


    def __request_handler_loop(self):
        print("Server now accepting connections")
        while True:
            client_socket, client_address = self.socket_in.accept()
            print("new client!")
            client_thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
            client_thread.start() 

    def __bind_socket_in(self, port):
        ip_temp = '127.0.0.1'
        self.socket_in.bind((ip_temp, port))
        print(f"socket binded to `{ip_temp}:{port}`")

if __name__ == "__main__":
    server = ChatServer()
    server.listen_to(6969) # TODO: pass by CLI arg instead













# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# log = Log()


# server_socket.bind(("0.0.0.0", 3000))

# server_socket.listen()
# log.info("Server is listening for incoming connections...")

# # username => client socket
# clients = {}

# # username => (username => ("message": <message>, "time": <timestamp>))
# messages = {}


# def parse_response(data):
#     lines = data.split('\n')
#     request_type = lines[0]

#     params = {}

#     for line in lines[1:]:
#         key, value = line.split(':', 1)
#         params[key.strip()] = value.strip()

#     return request_type, params


# def handle_client(client, address):
#     while True:
#         try:
#             data = client.recv(1024).decode()
#             request_type, params = parse_response(data)

#             # case 1: connecting
#             # type : CONNECT
#             # params : USERNAME
#             if request_type == "CONNECT":
#                 clients[params['USERNAME']] = client
#                 client.send(Status.SUCCESS.value.encode())

#                 log.info(f"User: {params['USERNAME']} {address} successfully connected")

#             # case 2: disconencting
#             # type : DISCONNECT
#             # params : USERNAME
#             if request_type == "DISCONNECT":
#                 del clients[params['USERNAME']]
#                 client.send(Status.SUCCESS.value.encode())

#                 log.info(f"User: {params['USERNAME']} {address} successfully disconnected")
#                 return

#             # case 3: sending message
#             # type : POST
#             # params: TO, MESSAGE
#             if request_type == "POST":
#                 timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
#                 message = params['MESSAGE']

#                 recipient_client = params['TO']


#         except:
#             continue


# while True:
#     client_socket, client_address = server_socket.accept()

#     client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
#     client_thread.start()
