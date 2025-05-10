#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
import json
from websockets.asyncio.client import connect


async def main():
    async with connect("ws://0.0.0.0:25565/join_room") as websocket:
        await websocket.send(json.dumps({
            "user_id": "NeoSahadeo",
            "room_id": "b22b51617dfe44b6a5c214a594d4bb75"
        }))
        # message = await websocket.recv()
        # print(message)


if __name__ == "__main__":
    asyncio.run(main())
