import asyncio
import json
import getpass
import urllib.request
import urllib.error
import websockets

async def main():
    base = "http://127.0.0.1:8001"
    login = input("Username or login: ")
    password = getpass.getpass("Password: ")

    payload = json.dumps({
        "login": login,
        "password": password,
    }).encode()

    request = urllib.request.Request(
        base + "/api/auth/login/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            login_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        print("Login failed:", exc.code)
        print(exc.read().decode())
        return
    except Exception as exc:
        print("Login request failed:", exc)
        return

    token = login_data.get("data", {}).get("access")
    if not token:
        print("Access token missing. Response keys:", list(login_data.keys()))
        return

    print("Login successful.")

    try:
        async with websockets.connect(
            "ws://127.0.0.1:8001/ws/events/"
        ) as ws:
            print("Server greeting:", await ws.recv())
            await ws.send(json.dumps({
                "type": "auth",
                "token": token,
            }))
            print("Authentication response:", await ws.recv())
    except Exception as exc:
        print("WebSocket test failed:", repr(exc))

if __name__ == "__main__":
    asyncio.run(main())
