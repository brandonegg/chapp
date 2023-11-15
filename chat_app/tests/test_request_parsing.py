from request import ChatAppRequest
from exceptions import UnparsableRequestException
import pytest

# INVALID REQUESTS:

def test_unparsable_action_line():
  """
  Test that with an unparsable action line, status 200 is raised
  """
  with pytest.raises(UnparsableRequestException) as error:
    ChatAppRequest("LOG\n")

  assert error.value.status_code == 200

def test_invalid_action():
  """
  Valid action line, but the action doesn't exist
  """
  with pytest.raises(UnparsableRequestException) as error:
    ChatAppRequest("REQUEST\tbrandon->server")

  assert error.value.status_code == 201

def test_missing_required_field():
  """
  Valid action line, but the action doesn't exist
  """
  with pytest.raises(UnparsableRequestException) as error:
    ChatAppRequest("RESPONSE\tserver->brandon")

  assert error.value.status_code == 204

def test_invalid_type_of_field_value():
  """
  Field value for status code has a string that isn't parsable as a number
  """
  with pytest.raises(UnparsableRequestException) as error:
    result = ChatAppRequest("RESPONSE\tserver->brandon\\\nstatus: hello")
  
  assert error.value.status_code == 202

# VALID REQUESTS:

def test_valid_introduce():
  """
  Valid introduction request
  """
  result = ChatAppRequest("INTRODUCE\tbrandon->server")

  assert result.type == "INTRODUCE"
  assert result.from_user == "brandon"
  assert result.to_user == "server"

def test_valid_response():
  """
  Valid response
  """
  result = ChatAppRequest("RESPONSE\tserver->brandon\\\nstatus: 200")
  
  assert result.type == "RESPONSE"
  assert result.from_user == "server"
  assert result.to_user == "brandon"
  assert "status" in result.fields
  assert result.fields["status"] == 200

def test_valid_request_with_complex_characters():
  """
  Includes a \n and : in message, both parsing characters of fields that should be valid.
  """
  result = ChatAppRequest("POST\tbrandon->server\\\nmessage: hello\nBrandon:brandon")
  
  assert result.fields["message"] == "hello\nBrandon:brandon"
