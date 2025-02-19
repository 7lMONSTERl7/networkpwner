import asyncio
import websockets
import readline

async def hello():
    url = "ws://127.0.1.1:8080"
    async with websockets.connect(url) as websocket:
        name = input(">>> ")
        await websocket.send(name)
        greeting = await websocket.recv()
        print(f"> {greeting}")

while True:
    asyncio.run(hello())