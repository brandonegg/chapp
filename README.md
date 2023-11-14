# Chatting Application Protocol

## Overview:

The protocol has the following format:

**Request:**
```
<ACTION>\t<FROM>-><TO>
status:<STATUS_CODE>
message:<STRING>
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
