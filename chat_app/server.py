import socket
import threading
import time
from exceptions import UnparsableRequestException
from request import ChatAppRequest
from request import Message
import logger
import json
import argparse

class ClientMap():
    def __init__(self):
        self.__username_socket_map = {}
        self.__messages: list[Message] = []

    def set_socket_username(self, username, socket):
        self.__username_socket_map[username] = socket
    
    def remove_socket_username(self, username):
        self.__username_socket_map[username] = None

    def username_taken(self, username):
        return username in self.__username_socket_map
    
    def username_not_taken(self, username):
        return not self.username_taken(username)
    
    def print_messages(self):
        print(self.__messages)

    def put_message(self, message: Message):
        self.__messages.append(message)
    
    def dump_messages(self):
        with open('chat_app/messages.json', 'w') as file:
            json.dump(self.__messages, file, default=str, indent=4)

    def find_messages(self, from_user: str, to_user: str) -> list[Message]:
        pass
        

class ChatServer():
    def __init__(self):
        self.socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = ClientMap()

    def listen_to(self, port: int):
        self.__bind_socket_in(port)
        self.socket_in.listen()
        self.__request_handler_loop()

    def handle_request(self, client_socket: socket.socket, client_address: str):
        listen = True
        while listen:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    continue

                try:
                    request = ChatAppRequest(data)
                except UnparsableRequestException as e:
                    response = ChatAppRequest()
                    response.type = "RESPONSE"
                    response.to_user = "unknown"
                    response.from_user = "server"
                    response.fields["status"] = e.status_code
                
                match request.type:
                    case "INTRODUCE":
                        self.__handle_introduce(request, client_socket)
                    case "POST":
                        self.__handle_post(request, client_socket)
                    case "GOODBYE": # TODO
                        # if goodbye is successful, end the loop
                        listen = self.__handle_goodbye(request, client_socket)
                        username = request.from_user
                        pass
                    case "RESPONSE":
                        pass # TODO
                    case _:
                        response = ChatAppRequest()
                        response.type = "RESPONSE"
                        response.to_user = "unknown"
                        response.from_user = "server"
                        response.fields["status"] = 201
            except:
                continue
        client_socket.close()
        self.clients.remove_socket_username(username)

    def __handle_post(self, request: ChatAppRequest, socket: socket.socket):
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"
        response.to_user = request.from_user
        response.fields["status"] = 200
        
        message = Message(time.strftime("[%Y-%m-%d %H:%M:%S]"), request.fields["message"], request.from_user, request.to_user)
        self.clients.put_message(message)

        logger.log_request(request)
        self.clients.dump_messages()

        # TODO does not send the message to the to_user!!!!
        # TODO does save the message!!!
        # TODO server does not load messages from messages.json!!!

        self.__send_response(response, socket)
        

    def __handle_introduce(self, request: ChatAppRequest, socket: socket.socket):
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"

        if self.clients.username_taken(request.from_user):
            response.to_user = "unknown"
            response.fields["status"] = 301
        else:
            self.clients.set_socket_username(request.from_user, socket)
            response.to_user = request.from_user
            response.fields["status"] = 200

        logger.log_request(request)

        self.__send_response(response, socket)
    
    def __handle_goodbye(self, request: ChatAppRequest, socket: socket.socket) -> bool:
        response = ChatAppRequest()
        response.type = "GOODBYE"
        response.from_user = "server"
        dont_end_loop = True

        response.to_user = request.from_user
        response.fields["status"] = 200
        dont_end_loop = False

        logger.log_request(request)

        self.__send_response(response, socket)
        return dont_end_loop


    def __send_response(self, response: ChatAppRequest, socket: socket.socket):
        socket.send(str(response).encode())

    def __request_handler_loop(self):
        print("Server now accepting connections")
        while True:
            client_socket, client_address = self.socket_in.accept()
            client_thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
            client_thread.start() 

    def __bind_socket_in(self, port):
        ip_temp = '127.0.0.1'
        self.socket_in.bind((ip_temp, port))
        print(f"socket binded to `{ip_temp}:{port}`")

if __name__ == "__main__":
    server = ChatServer()
    # copilot: take in port as a cli argument
    parser = argparse.ArgumentParser(description='Accept a port number')
    parser.add_argument('-p', '--port', type=int, default=6969, help='Port number')
    
    args = parser.parse_args()
    port_number = args.port

    server.listen_to(port_number)




