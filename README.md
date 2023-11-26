# Chatting Application Protocol

## Getting Started:
**Start the server:**
```sh
python .\chat_app\server.py
or
python3 .\chat_app\server.py
```

**Start a client:**
```sh
python .\chat_app\login.py
or
python3 .\chat_app\login.py
```

To send messages, on one login.py being run put in a name and submit, then either click on a previous dm's button or put in who you would like to dm and click the submit button. Then you can input a chat message and hit send and it will be seen on your GUI and the recipient's GUI if they are online. At any point, you can close the GUI, or hit the logout button and you will be able to log in again as that user. The same user can not be logged in at the same time as handled by the server.


**Running tests:**
```sh
sh ./bin/test
```

## Overview:

The protocol has the following format:

**Request:**
```
<ACTION>\t<FROM>-><TO>\\
status:<STATUS_CODE>\\
message:<STRING>\\
```

The first line of the request is called the *Action Line*, it is intended to specify the entire purpose of the data being sent and where it should go.
- ACTION = INTRODUCE|POST|RESPOND|DISCONNECT
- FROM = username of sending node
- TO = username of receiving node


Lines below this first line are called "fields" and are conditionally added based on action type.
```
<field>:<value>
```

For actions POST the following fields are required:
- message: The message being sent in the regular expression format: ".*+"


For actions RESPOND the following fields are required:
- status: A number representing the status of the previous request.


Actions INTRODUCE and DISCONNECT have no required fields.


### MISC notes to find a home for:
- Encoding is utf-8
- server responds with username = server. Only the server can be named server.
