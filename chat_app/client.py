import socket
import select
import json
from time import sleep
from request import ChatAppRequest
import argparse
from exceptions import UnparsableRequestException

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
  
  # todo: make this better, just made this wrapper for testing
  def handle_request(self):
    data = self.out_socket.recv(1024).decode()
    try:
      request = ChatAppRequest(data)
    except UnparsableRequestException as e:
      response = ChatAppRequest()
      response.type = "RESPONSE"
      response.to_user = "unknown"
      response.from_user = "server"
      response.fields["status"] = e.status_code

    match request.type:
      case "POST":
        print("Received post:")
        print(request)
        if request.to_user in self.messages:
          self.messages[request.to_user].append({"from": request.from_user, "message": request.fields["message"]})
        else:
          self.messages[request.to_user] = [{"from": request.from_user, "message": request.fields["message"]}]
        #tell server it went right
        response = ChatAppRequest()
        response.type = "RESPONSE"
        response.to_user = "server"
        response.from_user = self.username
        response.fields["status"] = 100
        self.__send_response(response)
      case "RESPONSE":
        print("received response")
        print(request)
        return request
      case "GOODBYE":
        print("received goodbye")
        print(request)
        return request
      case "INTRODUCE":
        print("received introduce")
        print(request)
        return request
      case _:
        print("received unknown request")
        print(request)
        return request
    
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

  def __send_response(self, response: ChatAppRequest):
    """
    Sends the request object over the socket

    Parameters
    ----------
    request : ChatAppRequest
      Request object to send
    """
    print("Sending:")
    print(response)
    self.out_socket.send(str(response).encode())

  def __wait_response(self, timeout:str = TIMEOUT_SEC) -> ChatAppRequest:
    try :
      # this is necessary because sometimes when the server sends all the messages
      # it is longer than 1024 bytes and otherwise the client will not receive all of it
      received_data = b''
      while True:
        chunk = self.out_socket.recv(1024)  # Receive up to 1024 bytes
        received_data += chunk  # Append the received chunk to the existing data
                
        if received_data.endswith(b'\\\n'):  # Check if the received data ends with a newline character
            break  # Break the loop if the data ends with a newline character

      decoded_data = received_data.decode()
      return ChatAppRequest(decoded_data)

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
  #use this for populating gui with messages
  data_string = response.fields["messages"]
  start_index = data_string.find("[")
  end_index = data_string.rfind("]") + 1
  messages_str = data_string[start_index:end_index]
  messages_str = messages_str.replace("'", '"')
  messages = json.loads(messages_str)
  # for example, if you wanted to print the third message
  #print(messages[2])

  
  # add this so if you run client with sam as username first you can test if it receives the post message from brandon
  while(username == "Sam"):
    chat_client.out_socket.setblocking(False)  # Set the socket to non-blocking mode, this means that the socket.recv() method will return immediately even if no data was received

    #this is an example of how all client threads can be listening for messages, while still being able to give a request if wanted
    ready_to_read, _, _ = select.select([chat_client.out_socket], [], [], 0.1)  # Check if the socket is ready to read
    if ready_to_read:
      chat_client.out_socket.setblocking(True)  # we want it to block now that we know there is data
      chat_client.handle_request()

    # you could put code right under here that has it do a request, so for example we could have a gui event listener here that
    # sends a post when the user hits enter on sending a message, even though it still is listening for messages

  response = chat_client.post("Sam", "yo")
  print(response)
  while(True):
    chat_client.out_socket.setblocking(False)  # Set the socket to non-blocking mode, this means that the socket.recv() method will return immediately even if no data was received

    #this is an example of how all client threads can be listening for messages, while still being able to give a request if wanted
    ready_to_read, _, _ = select.select([chat_client.out_socket], [], [], 0.1)  # Check if the socket is ready to read
    if ready_to_read:
      chat_client.out_socket.setblocking(True)  # we want it to block now that we know there is data
      chat_client.handle_request()

