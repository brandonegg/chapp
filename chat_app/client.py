import socket
import time
from request import ChatAppRequest
import argparse
import threading
import ast


TIMEOUT_SEC = 10


class ChatClient():
  def __init__(self, username: str):
    self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.username = username
    self.responses: list[ChatAppRequest] = []

    #list of all messages not in order
    self.messages: list[dict] = []


  def connect_to(self, ip: str, port: int) -> None:
    print(f"connecting to {ip}:{port}")
    self.out_socket.connect((ip, port))

    listening_thread = threading.Thread(target=self.client_loop, args=())
    listening_thread.start()


  def client_loop(self) -> None:
    received_data = b''
    self.out_socket.settimeout(5)  # Set a 5-second timeout
    while True:
      try:
        chunk = self.out_socket.recv(1024)  # Receive up to 1024 bytes
        received_data += chunk
                
        if received_data.endswith(b'\\\n'):  # Check if the received data ends with a newline character
            response = ChatAppRequest(received_data.decode())

            if response.type == "POST":
              self.messages.append(ast.literal_eval(response.fields["message"]))
            else:
              self.responses.append(response)
            received_data = b''
      except socket.timeout:
        print("Socket timed out!")
        return


  # gui needs to get the messages from the response.fields["messages"]
  def introduce(self) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = "server"
    request.type = "INTRODUCE"

    self.__send_request(request)
    return self.__wait_for_response(request.get_id())
  
  # gui needs to get the message (that was just posted) from the response.fields["message"]
  def post(self, to_user: str, message: str) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = to_user
    request.type = "POST"
    request.fields["message"] = message

    self.__send_request(request)
    return self.__wait_for_response(request.get_id())
  
  
  def goodbye(self) -> ChatAppRequest | None:
    request = ChatAppRequest()
    request.from_user = self.username
    request.to_user = "server"
    request.type = "GOODBYE"

    self.__send_request(request)
    return self.__wait_for_response(request.get_id())
        

  def __send_request(self, request: ChatAppRequest) -> None:
    print("Sending:")
    print(request)
    self.out_socket.send(str(request).encode())


  def __wait_for_response(self, id: int, timeout: int = TIMEOUT_SEC) -> ChatAppRequest | None:
    start_time = time.time()

    while True:
      current_time = time.time()

      if current_time - start_time > timeout:
        return None

      for res in self.responses:
        if res.fields["for"] == id:
          return res


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Accept a port number')
  parser.add_argument('-u', '--username', type=str, default="Brandon", help='Username to use for the chat client')
  parser.add_argument('-p', '--port', type=int, default=6969, help='Port number')
    
  args = parser.parse_args()
  username = args.username
  port_number = args.port


  chat_client = ChatClient("Brandon")
  chat_client.connect_to("127.0.0.1", port_number)

  response = chat_client.introduce()
  #print(response)

  response = chat_client.post("Sam", "im literally messaging rn")
  #print(response)

