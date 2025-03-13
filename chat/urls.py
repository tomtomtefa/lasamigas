from django.urls import path
from .views import chat_room, MessageListCreate, MessageDetail

urlpatterns = [
    path('', chat_room, name='chat-room'),
    path('messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
]
