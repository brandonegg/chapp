class UnparsableRequestException(Exception):
  def __init__(self, field_errors: dict[str, str]):
    # TODO: Convert field errors to message
    super().__init__("Invalid request")