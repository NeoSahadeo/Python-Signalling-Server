import json
import uuid
import asyncio
from websockets import ConnectionClosed
from websockets.asyncio.server import serve

HOST = "0.0.0.0"
PORT = 25565
ROOMS = {}
CLEAN = 60  # Seconds


async def clean_rooms():
    while True:
        print('Cleaning Vacant Rooms')
        empty_rooms = []
        for x in ROOMS:
            if len(ROOMS[x]["connections"]) == 0:
                empty_rooms.append(x)
        for x in empty_rooms:
            ROOMS.pop(x)
        await asyncio.sleep(CLEAN)


def dump_json(obj):
    try:
        return json.dumps(obj)
    except Exception as e:
        print(e)
        return {}


def load_json(_string):
    try:
        return json.loads(_string)
    except Exception as e:
        print(e)
        return {}


def generate_room(websocket, room_id=None):
    id = room_id or uuid.uuid4().hex
    if ROOMS.get(id):
        id = uuid.uuid4().hex

    ROOMS[id] = {
        "connections": [],
    }
    return id


def join_room(websocket, room_id):
    if ROOMS.get(room_id):
        if websocket not in ROOMS[room_id]["connections"]:
            ROOMS[room_id]["connections"].append(websocket)
        return True
    return False


async def resolve_path(websocket, message):
    if not message:
        return

    data = load_json(message)

    match websocket.request.path:
        case "/generate_room":
            room_id = data.get("room_id")
            if room_id:
                await websocket.send(json.dumps({"room_id": generate_room(websocket, room_id)}))
            else:
                await websocket.send(json.dumps({"room_id": generate_room(websocket, room_id)}))
            await websocket.close()

        case "/client_endpoint":
            room_id = data.get("room_id")
            message = data.get("message")
            if room_id and not message:  # If there is a room id but no message, then connect
                await websocket.send(json.dumps({"connected": join_room(websocket, room_id)}))
                return

            elif room_id and message:  # If there is both a room and and id, send a message
                for conn in ROOMS[room_id]["connections"]:
                    await conn.send(json.dumps({"message": message}))
                return


async def handler(websocket):
    try:
        while True:
            message = await websocket.recv()
            if websocket.request.path == "/":
                await websocket.send("Missing Path")
            else:
                await resolve_path(websocket, message)
    except ConnectionClosed:
        print("Client disconnected normally")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        for x in ROOMS:
            ROOMS[x]["connections"] = [
                conn for conn in ROOMS[x]["connections"] if conn != websocket
            ]


async def main():
    async with serve(handler, HOST, PORT):
        print(f"Signalling Server Started on {HOST}:{PORT}")
        print("Listening for connections...")
        asyncio.create_task(clean_rooms())

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
