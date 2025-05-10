import json
import uuid
import asyncio
from websockets import ConnectionClosed
from websockets.asyncio.server import serve

HOST = "0.0.0.0"
PORT = 25565

rooms = {
}


def generate_room(websocket, room_id=None):
    id = room_id or uuid.uuid4().hex
    rooms[id] = {
        "socket": websocket,
        # "time_left": 1440,
        "connections": [],
    }
    return json.dumps({"id": id})


async def join_room(websocket, room_id, user_id):
    if room_id == user_id:
        await websocket.send(json.dumps({
            "message": "You can't connect to yourself."
        }))
        await websocket.close()
        return

    if rooms.get(room_id) and rooms.get(user_id):
        rooms[room_id]["connections"].append({
            "id": user_id,
            "socket": websocket
        })
        for x in rooms:
            print(f"\n RoomID:{x}\n{rooms[x]["connections"]}\n")

    await websocket.close()


async def resolve_path(websocket, message):
    match websocket.request.path:
        case "/generate_room":
            if message:
                await websocket.send(generate_room(websocket), room_id=message)
            else:
                await websocket.send(generate_room(websocket))
            await websocket.close()
        case "/join_room":
            try:
                data = json.loads(message)
                room_id = data.get("room_id")
                user_id = data.get("user_id")
                if user_id and room_id:
                    await join_room(websocket, room_id, user_id)
            except json.decoder.JSONDecodeError:
                websocket.send(json.dumps({
                    "message": "Room ID or User ID not specified. Rejecting Offer"
                }))


async def handler(websocket):
    try:
        async for message in websocket:
            if websocket.request.path == "/":
                await websocket.send("Missing Path")
            else:
                await resolve_path(websocket, message)

    except ConnectionClosed:
        print("Client disconnected normally")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def main():
    async with serve(handler, HOST, PORT,
                     ping_interval=1,
                     ping_timeout=30,
                     close_timeout=10):
        print(f"Signalling Server Started on {HOST}:{PORT}")
        print("Listening for connections...")
        # await server.serve_forever()
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
