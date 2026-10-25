import os
import asyncio
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.layers import get_channel_layer

async def main():
    layer = get_channel_layer()
    print("Layer:", type(layer).__name__)

    await asyncio.wait_for(
        layer.send("ef.test", {
            "type": "test.message",
            "text": "hello",
        }),
        timeout=10,
    )
    print("SEND OK")

    message = await asyncio.wait_for(
        layer.receive("ef.test"),
        timeout=10,
    )
    print("RECEIVE OK:", message)

if __name__ == "__main__":
    asyncio.run(main())
