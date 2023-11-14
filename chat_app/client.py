import socket
from request import ChatAppRequest

TIMEOUT_SEC = 10

class ChatClient():
  def __init__(self, username: str):
    self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.username = username

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
  
  def post(self, recipient: str, message: str) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = recipient
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
    return ChatAppRequest(self.out_socket.recv(1024).decode())

if __name__ == "__main__":
  chat_client = ChatClient("Brandon")
  chat_client.connect_to("127.0.0.1", 6969)
  response = chat_client.introduce()
  print(response)

  response = chat_client.post("Sam", "hi")
  print(response)
