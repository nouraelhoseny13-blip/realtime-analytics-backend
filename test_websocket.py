import asyncio
import websockets


async def test():
    async with websockets.connect(
        "ws://127.0.0.1:8000/api/ws/analytics"
    ) as ws:
        message = await ws.recv()
        print(message)


asyncio.run(test())