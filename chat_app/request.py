from exceptions import UnparsableRequestException


REQUEST_TYPE_REQUIRED_FIELD_MAPS: dict[str, set[str]] = {
    "INTRODUCE": set(),
    "RESPONSE": {"status", "for"},
    "POST": {"message"},
    "GOODBYE": set()
}


STATUS_CODE_MAP = {
    100: "SUCCESS", # TRANSPORT SUCCESS 100-199
    200: "UNPARSABLE_ACTION", # PARSE ERRORS 200-299
    201: "INVALID_ACTION",
    202: "UNPARSABLE_FIELD",
    203: "DUPLICATE_FIELD",
    204: "MISSING_REQUIRED_FIELD",
    205: "MALFORMED_ID_LINE",
    301: "USERNAME_TAKEN", # INVALID INPUT ERRORS 300-399
    302: "INVALID_TO_USER",
    303: "INVALID_FROM_USER",
    304: "NOT_INTRODUCED",
    400: "SERVER_ERROR",
}


FIELD_TYPE_MAP = {
    "status": int,
    "message": str,
    "for": int,
    "id": int
}


class ChatAppRequest():
    __next_id = 0

    def __init__(self, body: str = None):
        self.type: str = None
        self.to_user: str = None
        self.from_user: str = None
        self.__id: int = None
        self.fields: dict[str, ] = {}

        if body:
            self.from_body(body)
        else:
            self.__id = self.__get_next_id()


    def get_id(self) -> int:
        return self.__id
    
    
    def __get_next_id(self) -> int:
        id = ChatAppRequest.__next_id
        ChatAppRequest.__next_id += 1
        return id


    def from_body(self, body: str) -> None:
        if len(body) == 0:
            raise UnparsableRequestException(200, "Message body empty")
        lines = body.split("\\\n")

        self.__parse_action_line(lines[0])

        if len(lines) > 1:
            self.__parse_fields(lines[1:])

        if "id" in self.fields:
            self.__id = self.fields["id"]

        self.__validate_request()


    def __parse_action_line(self, line: str) -> None:
        split = line.split("\t")
        if not len(split) == 2:
            raise UnparsableRequestException(200, "Action line unreadable")
        
        type = split[0].upper()
        path_str = split[1].split("->")

        if not len(path_str) == 2:
            raise UnparsableRequestException(200, "from->to relation invalid")
        
        self.type = type
        self.from_user = path_str[0]
        self.to_user = path_str[1]


    def __validate_request(self) -> None:
        # Validate type is real
        if not self.type in REQUEST_TYPE_REQUIRED_FIELD_MAPS:
            raise UnparsableRequestException(201, f"Action type `{self.type}` unacceptable")

        # Validate required fields are present
        if not REQUEST_TYPE_REQUIRED_FIELD_MAPS[self.type].issubset(set([field for field in self.fields])):
            raise UnparsableRequestException(204, f"Required field missing from {self.fields}")
        
        if self.__id is None:
            raise UnparsableRequestException(205, "Missing ID line")


    def __parse_fields(self, lines: list[str]) -> None:
        pairs = {}

        for field_line in lines:
            # need this check, I had to add a newline to the end of the string
            # for the client to receive all the data
            if field_line != '':
                split_line = field_line.split(":")

                if len(split_line) < 2:
                    raise UnparsableRequestException(202, f"Unreadable field-value pair passed")

                label = split_line[0].lower()
                value = ":".join(split_line[1:]).lstrip()

                if label in self.fields:
                    raise UnparsableRequestException(203, f"duplicate field `{split_line[0].lower()}`")

                if split_line[0] in FIELD_TYPE_MAP:
                    try:
                        value = FIELD_TYPE_MAP[label](value)
                    except:
                        raise UnparsableRequestException(202, f"Unreadable field-value pair passed")

                pairs[label] = value

        self.fields = pairs


    def __str__(self) -> str:
        fieldlines = [f"{field}: {str(self.fields[field])}" for field in self.fields]
        
        return "\\\n".join([
            f"{self.type}\t{self.from_user}->{self.to_user}",f"ID:{self.__id}",
            *fieldlines
        ])
    