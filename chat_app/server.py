import socket
import threading
import time
from exceptions import UnparsableRequestException
from request import ChatAppRequest
import logger
import json
import argparse


class ClientMap():
    def __init__(self):
        self.__username_socket_map: dict[str, socket.socket] = {}
        self.__messages: list[dict[str, str]] = []


    def set_socket_username(self, username, socket) -> None:
        self.__username_socket_map[username] = socket


    def get_socket_by_username(self, username: str) -> socket.socket:
        return self.__username_socket_map[username]
    

    def remove_socket_by_username(self, username) -> None:
        del self.__username_socket_map[username]


    def remove_socket(self, socket: socket.socket) -> None:
        for key, value in self.__username_socket_map.items():
                if value == socket:
                    self.remove_socket_by_username(key)
                    return
        socket.close()


    def username_taken(self, username) -> bool:
        return username in self.__username_socket_map
    

    def print_messages(self) -> None:
        print(self.__messages)


    def put_message(self, message: dict[str, str]) -> None:
        self.__messages.append(message)
    

    def dump_messages(self) -> None:
        with open("chat_app/messages.json", 'w') as file:
            json.dump(self.__messages, file, indent=4)
    

    def find_messages(self, user: str) -> list[dict[str, str]]:
        return [msg for msg in self.__messages 
                if msg["from_user"] == user or msg["to_user"] == user]
    
    
    def load_messages(self) -> None:
        try:
            with open("chat_app/messages.json", 'r') as file:
                self.__messages = json.load(file)

        except FileNotFoundError:
            print("File not found. Creating a new file.")

            with open("chat_app/messages.json", 'w') as file:
                file.write('[]')
                self.__messages = []

        except json.JSONDecodeError:
            print("Invalid JSON format in the file. Wiping the file.")

            with open("chat_app/messages.json", 'w') as file:
                file.write('[]')
                self.__messages = []
        

class ChatServer():
    def __init__(self):
        self.socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = ClientMap()


    def listen_to(self, port: int) -> None:
        self.__bind_socket_in(port)
        self.socket_in.listen()
        self.clients.load_messages()
        self.__request_handler_loop()


    def handle_request(self, client_socket: socket.socket) -> None:
        while True:
            try:
                data = client_socket.recv(1024).decode()

                try:
                    request = ChatAppRequest(data)
                except UnparsableRequestException as e:
                    response = ChatAppRequest()
                    response.type = "RESPONSE"
                    response.to_user = "unknown"
                    response.from_user = "server"
                    response.fields["status"] = e.status_code

                    logger.log_response(response)
                    
                logger.log_request(request)
                
                match request.type:
                    case "INTRODUCE":
                        self.__handle_introduce(request, client_socket)
                    case "POST":
                        self.__handle_post(request, client_socket)
                    case "GOODBYE":
                        self.__handle_goodbye(request, client_socket)
                        return
                    case _:
                        response = ChatAppRequest()
                        response.type = "RESPONSE"
                        response.to_user = "unknown"
                        response.from_user = "server"
                        response.fields["status"] = 201

                        logger.log_response(response)

            except Exception as e:
                # if any exception occurs we print it and properly disconnect the socket
                print(e)
                self.clients.remove_socket(client_socket)
                return


    def __handle_introduce(self, request: ChatAppRequest, socket: socket.socket) -> None:
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"
        response.fields["for"] = request.get_id()

        if self.clients.username_taken(request.from_user):
            response.to_user = "unknown"
            response.fields["status"] = 301

        else:
            self.clients.set_socket_username(request.from_user, socket)
            response.to_user = request.from_user
            response.fields["status"] = 100

            messages = self.clients.find_messages(request.from_user)
            response.fields["messages"] = messages

        self.__send_response(response, socket)

    
    def __handle_post(self, request: ChatAppRequest, socket: socket.socket) -> None:
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"
        response.fields["for"] = request.get_id()

        if self.clients.username_taken(request.from_user):
            response.to_user = request.from_user

            message = {
                "timestamp": time.strftime("[%Y-%m-%d %H:%M:%S]"),
                "message": request.fields["message"],
                "from_user": request.from_user,
                "to_user": request.to_user
            }

            if (self.clients.username_taken(request.to_user)):
                request.fields["message"] = message
                self.__send_response(request, self.clients.get_socket_by_username(request.to_user))
            
            response.fields["status"] = 100
            response.fields["message"] = message

            self.clients.put_message(message)
            self.clients.dump_messages()

        else:
            response.to_user = "unknown"
            response.fields["status"] = 304


        self.__send_response(response, socket)

    
    def __handle_goodbye(self, request: ChatAppRequest, socket: socket.socket) -> None:
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"
        response.to_user = request.from_user
        response.fields["status"] = 100
        response.fields["for"] = request.get_id()

        self.clients.remove_socket(socket)


        self.__send_response(response, socket)


    def __send_response(self, response: ChatAppRequest, socket: socket.socket) -> None:
        logger.log_response(response)
        socket.send((str(response) + "\\\n").encode())


    def __request_handler_loop(self) -> None:
        print("Server now accepting connections")
        while True:
            client_socket, client_address = self.socket_in.accept()
            client_thread = threading.Thread(target=self.handle_request, args=(client_socket,))
            client_thread.start() 


    def __bind_socket_in(self, port) -> None:
        ip_temp = '127.0.0.1'
        self.socket_in.bind((ip_temp, port))
        print(f"socket binded to `{ip_temp}:{port}`")


if __name__ == "__main__":
    server = ChatServer()
    parser = argparse.ArgumentParser(description='Accept a port number')
    parser.add_argument('-p', '--port', type=int, default=6969, help='Port number')
    
    args = parser.parse_args()
    port_number = args.port

    server.listen_to(port_number)
