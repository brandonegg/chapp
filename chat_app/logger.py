from request import ChatAppRequest

def print_border_bottom(message: str):
  print(message)
  print("-------------------------------")

def log_request(request: ChatAppRequest):
  print("Received request:")
  print_border_bottom(request)

def log_response(response: ChatAppRequest):
  print("Sending response:")
  print_border_bottom(response)

def log_send_request(request: ChatAppRequest):
  print("Sending request:")
  print_border_bottom(request)

def log_receive_response(response: ChatAppRequest):
  print("Received response:")
  print_border_bottom(response)