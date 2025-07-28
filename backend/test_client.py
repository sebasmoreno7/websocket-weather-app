# test_client.py
import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws/observer"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Test desde Python")
        while True:
            msg = await websocket.recv()
            print("💬 Recibido:", msg)

asyncio.run(test_ws())
