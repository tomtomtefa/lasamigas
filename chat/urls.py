from django.urls import path
from .views import MessageListCreateView, private_chat, test_messages_api  # ✅ Vérifie les imports

urlpatterns = [
    path("messages/", MessageListCreateView.as_view(), name="message-list-create"),  # ✅ Doit être AVANT `private_chat`
    path("test-api/", test_messages_api, name="test-api"),  # ✅ Doit être AVANT `private_chat`
    path("<str:username>/", private_chat, name="private-chat"),  # ✅ Cette route doit être en dernier
]
