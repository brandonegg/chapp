# Chatting Application Protocol

## Overview:

The protocol has the following format:

**Request:**
```
<ACTION>\t<FROM>-><TO>
status: <STATUS_CODE>
message: <STRING>
```

**Response:**
```
{type=INTRODUCE|POST}\t{username field}
timestamp: str-iso format
message: str
```


### MISC notes to find a home for:
- Encoding is utf-8
- server responds with username = server. Only the server can be named server.



client connection:
CONNECT
USERNAME:<username>

client disconnection:
DISCONNECT
USERNAME:<username>

client sending message:
POST
TO:<username>
MESSAGE:<message>

server success:
200

server side error:
400
