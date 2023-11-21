import socket
from request import ChatAppRequest
import argparse

TIMEOUT_SEC = 10

class ChatClient():
  def __init__(self, username: str):
    self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.username = username

    #recipient => list of messages between user and recipient
    self.messages: dict[str, list[dict[str, str]]] = {}

  def connect_to(self, ip: str, port: int):
    print(f"connecting to {ip}:{port}")
    self.out_socket.connect((ip, port))

  def introduce(self) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = "server"
    request.type = "INTRODUCE"

    self.__send_request(request)
    return self.__wait_response()
  
  def goodbye(self) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = "server"
    request.type = "GOODBYE"

    self.__send_request(request)
    return self.__wait_response()
  
  def post(self, to_user: str, message: str) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = to_user
    request.type = "POST"
    request.fields["message"] = message

    self.__send_request(request)
    return self.__wait_response()

    
  def __clear_incomming(self):
    """
    Clears the incoming socket requests sent earlier but no longer relevant
    """
    pass

  def __send_request(self, request: ChatAppRequest):
    """
    Sends the request object over the socket

    Parameters
    ----------
    request : ChatAppRequest
      Request object to send
    """
    print("Sending:")
    print(request)
    self.out_socket.send(str(request).encode())

  def __wait_response(self, timeout:str = TIMEOUT_SEC) -> ChatAppRequest:
    try :
      return ChatAppRequest(self.out_socket.recv(1024).decode())
    except ConnectionAbortedError as e:
      # Handle the case when the connection is closed by the server
      # For instance, stop trying to send/receive data through this socket
      print("Connection closed by the server.")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Accept a port number')
  parser.add_argument('-u', '--username', type=str, default="Brandon", help='Username to use for the chat client')
  parser.add_argument('-p', '--port', type=int, default=6969, help='Port number')
    
  args = parser.parse_args()
  username = args.username
  port_number = args.port


  chat_client = ChatClient(username)
  chat_client.connect_to("127.0.0.1", port_number)

  response = chat_client.introduce()
  print(response)

  response = chat_client.post("Sam", "yo")
  print(response)

