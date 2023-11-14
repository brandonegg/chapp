import socket
from request import ChatAppRequest

TIMEOUT_SEC = 10

class ChatClient():
  def __init__(self):
    self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect_to(self, ip: str, port: int):
    print(f"connecting to {ip}:{port}")
    self.out_socket.connect((ip, port))

  def introduce(self, username: str) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = username
    request.to_user = "server"
    request.type = "INTRODUCE"

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

  def __wait_response(self, timeout:str) -> ChatAppRequest:
    return ChatAppRequest(self.out_socket.recv(1024).decode())

if __name__ == "__main__":
  chat_client = ChatClient()
  chat_client.connect_to("127.0.0.1", 6969)
  response = chat_client.introduce("Brandon")
  print(response)