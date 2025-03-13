import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_general"
        self.channel_layer = self.channel_layer  # ⚠️ Ajoute cette ligne
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("✅ WebSocket connecté")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("⚠️ WebSocket déconnecté")

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name, 
            {"type": "chat_message", "message": data["message"]}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
        print(f"📤 Message envoyé à tous : {event['message']}")
