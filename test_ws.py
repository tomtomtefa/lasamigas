import os
import django
from channels.layers import get_channel_layer
import asyncio

# Charger Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dating_app.settings")
django.setup()

# Tester WebSocket
async def test_websocket():
    layer = get_channel_layer()
    await layer.group_send("chat_chat", {"type": "chat.message", "message": "Test Message WebSocket"})

asyncio.run(test_websocket())
print("✅ Message envoyé au WebSocket !")

