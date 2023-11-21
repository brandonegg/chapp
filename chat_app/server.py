import socket
import threading
import time
from exceptions import UnparsableRequestException
from request import ChatAppRequest
#from request import Message
import logger
import json
import argparse

class ClientMap():
    def __init__(self):
        self.__username_socket_map:dict = {}
        self.__messages: list[dict[str, str]] = []

    def get_iterable_username_socket_map(self):
        return self.__username_socket_map.items()

    def set_socket_username(self, username, socket):
        self.__username_socket_map[username] = socket

    def get_socket_by_username(self, username: str) -> socket.socket:
        return self.__username_socket_map[username]
    
    def remove_socket_username(self, username):
        self.__username_socket_map[username] = None

    def username_taken(self, username):
        return username in self.__username_socket_map
    
    def username_not_taken(self, username):
        return not self.username_taken(username)
    
    def print_messages(self):
        print(self.__messages)

    def put_message(self, message: dict[str, ]):
        self.__messages.append(message)
    
    def dump_messages(self):
        with open("chat_app/messages.json", 'w') as file:
            json.dump(self.__messages, file, indent=4)
    
    def find_messages(self, user: str) -> list[dict[str, str]]:
        return [msg for msg in self.__messages if msg["from_user"] == user or msg["to_user"] == user]
    
    def load_messages(self):
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

    def listen_to(self, port: int):
        self.__bind_socket_in(port)
        self.socket_in.listen()
        self.clients.load_messages()
        self.__request_handler_loop()

    def handle_request(self, client_socket: socket.socket, client_address: str):
        listen = True
        while listen:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    #todo make this remove the user that has this socket from the map
                    #only get here if an empty string is sent which happens when the client
                    #disconnects without a goodbye
                    #go through self.__username_socket_map and remove the socket that is equal to client_socket
                    # for key, value in self.clients.get_iterable_username_socket_map():
                    #     print(key, value)
                    #     print(client_socket)
                    #     if value == client_socket:
                    #         #self.clients.__username_socket_map[key] = None
                    #         print("found it", key, value)
                    continue

                try:
                    request = ChatAppRequest(data)
                except UnparsableRequestException as e:
                    response = ChatAppRequest()
                    response.type = "RESPONSE"
                    response.to_user = "unknown"
                    response.from_user = "server"
                    response.fields["status"] = e.status_code

                    logger.log_request(response)
                
                match request.type:
                    case "INTRODUCE":
                        self.__handle_introduce(request, client_socket)
                    case "POST":
                        self.__handle_post(request, client_socket)
                    case "GOODBYE":
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

                        logger.log_request(response)
            except Exception as e:
                print(e)
                #todo this needs to be fixed it would catch all exceptions and do nothing about them lol
                continue
        client_socket.close()
        self.clients.remove_socket_username(username)

    def __handle_post(self, request: ChatAppRequest, socket: socket.socket):
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.from_user = "server"
        response.to_user = request.from_user
        

        if self.clients.username_taken(request.from_user):

            message = {
                "timestamp": time.strftime("[%Y-%m-%d %H:%M:%S]"),
                "message": request.fields["message"],
                "from_user": request.from_user,
                "to_user": request.to_user
            }
            
            self.clients.put_message(message)
            self.clients.dump_messages()


            response.fields["messages"] = str(self.clients.find_messages(request.from_user)) + "\\\n"
            if(self.clients.username_taken(request.to_user)):
                #self.__send_response(request, self.clients.get_socket_by_username(request.to_user))
                response.fields["status"] = 100
                response.fields["status"] = 100
            else:
                response.fields["status"] = 401


        else:
            response.to_user = "unknown"
            response.fields["status"] = 301

        logger.log_request(request)

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
            response.fields["status"] = 100
            response.fields["status"] = 100

            messages = self.clients.find_messages(request.from_user)
            response.fields["messages"] = str(messages) + "\\\n"

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
        logger.log_response(response)
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




