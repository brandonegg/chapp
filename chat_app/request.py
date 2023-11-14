from exceptions import UnparsableRequestException
import time

REQUEST_TYPE_REQUIRED_FIELD_MAPS: dict[str, set[str]] = {
    "INTRODUCE": set(),
    "RESPONSE": {"status"},
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
    301: "USERNAME_TAKEN", # INVALID INPUT ERRORS 300-399
    302: "INVALID_TO_USER",
    303: "INVALID_FROM_USER"
}


FIELD_TYPE_MAP = {
    "status": int,
    "message": str,
}

class Message():
    def __init__(self, timestamp, message: str):
        self.timestamp = timestamp
        self.message = message

class ChatAppRequest():
    def __init__(self, body: str | None = None):
        self.type: str = None
        self.to_user: str = None
        self.from_user: str = None
        self.fields: dict[str, ] = {}

        if not body is None:
            self.from_body(body)

    def add_field(self, key: str, value):
        self.fields[key] = value

    def from_body(self, body: str):
        if len(body) == 0:
            raise UnparsableRequestException(200, "Message body empty")
        
        lines = body.split("\n")
        self.__parse_action_line(lines[0])

        if len(lines) > 1:
            self.__parse_fields(lines[1:])

        self.__validate_request()

    def __parse_action_line(self, line: str):
        """
        Parses action line and sets instance variables action, from, and
        to based on input. This function DOES NOT verify the validity of
        passed values, but does verify that it is parsible.

        Parameters
        ----------
        line : str
            The action line to parse

        Raises
        ------
        UnparsableRequestException
            When action line is unparsible
        """
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

    def __validate_request(self):
        """
        Checks that request object meets valid request criteria.

        Raises
        ------
        UnparsableRequestException
            When an instance variable of the request object is invalid.
        """
        # Validate type is real
        if not self.type in REQUEST_TYPE_REQUIRED_FIELD_MAPS:
            raise UnparsableRequestException(201, f"Action type `{self.type}` unacceptable")

        # Validate required fields are present
        if not REQUEST_TYPE_REQUIRED_FIELD_MAPS[self.type].issubset(set([field for field in self.fields])):
            raise UnparsableRequestException(204, f"Required field missing")


    def __parse_fields(self, lines: list[str]):
        """
        Raises
        ------
        UnparsableRequestException
            When field value line is unparsable.
        """
        pairs = {}

        for field_line in lines:
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
        """
        Convert instance to string sent over socket. This function does check the validty
        of passed fields, but does verify parsibility

        Returns
        -------
        string
            Request string
        """
        fieldlines = [f"{field}: {str(self.fields[field])}" for field in self.fields]
        
        return "\n".join([
            f"{self.type}\t{self.from_user}->{self.to_user}",
            *fieldlines
        ])
