from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from users.models import UserProfile

# ✅ Vue pour afficher la liste des chats
@login_required
def chat_room(request):
    return render(request, "chat/chat_room.html")  # Assure-toi que ce fichier existe

# ✅ Vue pour la messagerie privée
@login_required
def private_chat(request, username):
    other_user = get_object_or_404(UserProfile, username=username)

    # Récupération des messages entre les deux utilisateurs
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    messages = messages.order_by("timestamp")

    print(f"Rendering private_chat.html for {other_user.username}")  # Debugging

    return render(request, "chat/private_chat.html", {"other_user": other_user, "messages": messages})

# ✅ Vue API pour récupérer et envoyer des messages
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
