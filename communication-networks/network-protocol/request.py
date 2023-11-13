import exceptions

REQUEST_TYPES = ["INTRODUCE", "POST", "GOODBYE"]
STATUS_CODE_MAP = {
    100: "POST_ACK", # TRANSPORT SUCCESS 100-199
    102: "INTRODUCE_ACK",
    103: "GOODBYE_ACK",
    200: "POST_NACK", # TRANSPORT ERRORS 200-299
    201: "GOODBYE_NACK",
    202: "INTRODUCE_NACK",
    301: "USERNAME_TAKEN", # INVALID INPUT ERRORS 300-399
    302: "MESSAGE_EMPTY"
}


VALID_ARGS = {
    
}

class ChatAppRequest():
    def __init__(self, body: str):
        lines = body.split("\n")

        self.__parse_action_line(lines)

    def __parse_action_line(self, line: str):
        split = line.split("\t")
        if len(split) > 2:
            raise exceptions.UnparsableRequestException({"action_line": "Unexpected length of action line"})

class ChatAppResponse():
    def __init__(self, body):
        self.status = 