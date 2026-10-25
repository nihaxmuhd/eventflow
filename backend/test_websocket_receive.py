import asyncio
import json
import websockets

async def main():
    token = input("Paste a fresh access token: ").strip()

    async with websockets.connect("ws://127.0.0.1:8001/ws/events/") as ws:
        print("Greeting:", await ws.recv())
        await ws.send(json.dumps({"type": "auth", "token": token}))
        print("Auth:", await ws.recv())
        print("Waiting for an event... Press Ctrl+C to stop.")

        while True:
            print("Received:", await ws.recv())

if __name__ == "__main__":
    asyncio.run(main())
