![Python Signalling Server Image](https://i.imgur.com/Pozt5iE.png)

# Python Signalling Server


This is a Python signalling server that uses rooms to connect clients together.

It uses [Python Websockets](https://websockets.readthedocs.io/en/stable/) to handle the socket connections, messages and disconnects.
## Documentation

I have tried to document most things here. The actual code isn't crazy and hopefully is quite easy to read through!

> All endpoints take in a message. The client MUST send a message for the websocket to respond; even if the message is nothing.


### Generating a room

To generate a room one should send a socket message to the `ws://[URI]/generate_room`. This will send a message back to the client with the room id. Share this room id with other clients to connect to the same room.

One can optionally specify a room id by send that in the message, for example: `{"room_id": "A super custom room name"}`

The connection will immediately be closed because the only function of the endpoint is to generate a room id.

### Connecting to a room

To connect to a room one should use the `ws://[URI]/client_endpoint` and send a room id message.

If the room exists, a message will be send back to the client with a status, eg: `{"connection": true}` if successful.

#### Messaging

This will keep a connection open on which the client can send messages. Once opened, the client socket can send messages by including a message similar to `{"message": "Hello everynan!"}`. This message will then be sent to every connection in the room.

### Disconnecting from a room / Disconnecting a client

To do this, the client has to send a disconnect signal from the their socket or simply close the active application.
## Authors

- [@NeoSahadeo](https://www.github.com/NeoSahadeo)


## Contributing

Contributions are always welcome!
