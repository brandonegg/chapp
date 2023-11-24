from request import ChatAppRequest
from request import STATUS_CODE_MAP as map


def print_border_bottom(message: str) -> None:
  print(message)
  print("-------------------------------")


def log_request(request: ChatAppRequest) -> None:
  print("Received request:")
  print_border_bottom(request)


def log_response(response: ChatAppRequest) -> None:
  print("Sending response:")
  print_border_bottom(response)
  #print(map.get(response.fields["status"]))
