from chat_app.request import ChatAppRequest
from chat_app.exceptions import UnparsableRequestException
import pytest

def test_unparsable_action_line():
  """
  Test that with an unparsable action line, status 200 is raised
  """
  with pytest.raises(UnparsableRequestException):
    ChatAppRequest().from_body(
      "LOG\n"
    )