# Chatting Application Protocol

## Getting Started:
> Note: python may be referred to python3 on your system. The two are typically interchangable and dependent on your system path configuration. If python does not work, you may try python3

#### Start the server:

**_windows_:**
```sh
python .\chat_app\server.py
```
**_linux/macos_:**
```sh
sh ./bin/start.sh server
```

#### Start a client:

**_windows_:**
```sh
python .\chat_app\login.py
```
**_linux/macos_:**
```sh
sh ./bin/start.sh client
```


To send messages, on one login.py being run put in a name and submit, then either click on a previous dm's button or put in who you would like to dm and click the submit button. Then you can input a chat message and hit send and it will be seen on your GUI and the recipient's GUI if they are online. At any point, you can close the GUI, or hit the logout button and you will be able to log in again as that user. The same user can not be logged in at the same time as handled by the server.


**Running tests:**
We have included several test cases for validating the protocol message parser (ChatAppRequest class). The tests are run with pytest using the shollowing command.

```sh
sh ./bin/test
```

## Overview:

The protocol has the following format:

**Request:**
```
<ACTION>\t<FROM>-><TO>\
{field key}: {field value}
...
```

The first line of the request is called the *Action Line*, it is intended to specify the entire purpose of the data being sent and where it should go.
- ACTION = INTRODUCE|POST|RESPOND|DISCONNECT
- FROM = username of sending node
- TO = username of receiving node


Lines below this first line are called "fields" and are conditionally added based on action type.
```
<field>:<value>
```

#### General Field Rules:

- All requests require an id field.
- For actions POST the following fields are required:
  - message: The message being sent in the regular expression format: ".*+"
- For actions RESPOND the following fields are required:
  - status: A number representing the status of the previous request.
- Actions INTRODUCE and DISCONNECT have no required fields other than id.
