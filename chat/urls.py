from django.urls import path
from .views import chat_room, private_chat, MessageListCreateView

urlpatterns = [
    path("", chat_room, name="chat-room"),  # ✅ Page principale du chat
    path("<str:username>/", private_chat, name="private-chat"),  # ✅ Messagerie privée (Correction ici)
    path("messages/", MessageListCreateView.as_view(), name="message-list-create"),  # ✅ API pour gérer les messages
]
