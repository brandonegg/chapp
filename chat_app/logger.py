from request import ChatAppRequest

def print_border_bottom(message: str):
  print(message)
  print("-------------------------------")

def log_request(request: ChatAppRequest):
  print("Received request:")
  print_border_bottom(request)