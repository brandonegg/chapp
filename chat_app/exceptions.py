class UnparsableRequestException(Exception):
  def __init__(self, status_code: int, message: str):
    super().__init__(message)

    self.status_code = status_code
