from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
from django.shortcuts import render

def chat_room(request):
    context = {}  # 👈 Ajoute ce dictionnaire pour éviter les erreurs
    return render(request, 'chat.html', context)

