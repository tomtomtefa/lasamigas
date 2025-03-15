from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Message
from .serializers import MessageSerializer
from users.models import UserProfile


@login_required
def chat_room(request):
    """Affiche la liste des discussions"""
    return render(request, "chat/chat_room.html")


@login_required
def private_chat(request, username):
    """Affiche la messagerie privée entre deux utilisateurs"""
    try:
        other_user = get_object_or_404(UserProfile, username=username)
        print(f"✅ DEBUG: Utilisateur trouvé - {other_user.username} (ID: {other_user.id})")
    except UserProfile.DoesNotExist:
        print(f"❌ DEBUG: Utilisateur {username} introuvable.")
        return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user)) |
        (Q(sender=other_user, receiver=request.user))
    ).order_by("timestamp")

    print(f"🔍 DEBUG: Chargement des messages entre {request.user.username} et {other_user.username} ({messages.count()} messages)")

    return render(request, "chat/private_chat.html", {"other_user": other_user, "messages": messages})


class MessageListCreateView(generics.ListCreateAPIView):
    """Vue API pour récupérer et envoyer des messages entre deux utilisateurs"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Récupère uniquement les messages privés entre l'utilisateur connecté et l'autre utilisateur"""
        other_user_id = self.request.GET.get("other_user_id")

        # Vérification et conversion de l'ID utilisateur
        try:
            other_user_id = int(other_user_id)  # ✅ Convertir en entier avant la requête
            other_user = get_object_or_404(UserProfile, id=other_user_id)
            print(f"✅ DEBUG: Utilisateur trouvé - {other_user.username} (ID: {other_user.id})")
        except (ValueError, TypeError):
            print(f"❌ DEBUG: `other_user_id` invalide : {other_user_id}")
            return JsonResponse({"error": "ID utilisateur invalide"}, status=400)
        except UserProfile.DoesNotExist:
            print(f"❌ DEBUG: Utilisateur ID {other_user_id} introuvable.")
            return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

        print(f"🔍 DEBUG: Recherche des messages entre {self.request.user.username} et {other_user.username}")

        messages = Message.objects.filter(
            (Q(sender=self.request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=self.request.user))
        ).order_by("timestamp")

        print(f"✅ DEBUG: {messages.count()} messages trouvés entre {self.request.user.username} et {other_user.username}")
        return messages

    def perform_create(self, serializer):
        """Enregistre un message en vérifiant les permissions et l'existence du destinataire"""
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Vous devez être connecté pour envoyer un message.")

        receiver_id = self.request.data.get("receiver")

        # Vérification de l'ID du destinataire
        try:
            receiver_id = int(receiver_id)
            receiver = get_object_or_404(UserProfile, id=receiver_id)
        except (ValueError, TypeError):
            print(f"❌ DEBUG: `receiver_id` invalide : {receiver_id}")
            return Response({"error": "ID du destinataire invalide"}, status=400)

        print(f"📩 DEBUG: Envoi d'un message de {self.request.user.username} vers {receiver.username}")

        serializer.save(sender=self.request.user, receiver=receiver)
        return Response(serializer.data, status=201)  # ✅ Réponse JSON explicite


def test_messages_api(request):
    """Vue de test pour voir si l'API fonctionne."""
    print("✅ DEBUG: `test-api` a bien été appelé !")
    return JsonResponse({"status": "success", "message": "API accessible"})
