from django.shortcuts import render
from users.models import UserProfile  # 👈 Import du modèle des utilisateurs

def home(request):
    return render(request, 'index.html')  # 👈 Affiche la page d'accueil

def user_list(request):
    users = UserProfile.objects.all()  # 👈 Récupère tous les utilisateurs
    return render(request, 'users.html', {'users': users})  # 👈 Envoie les utilisateurs au template

from django.http import JsonResponse

def test_messages_api(request):
    return JsonResponse({"status": "success", "message": "API accessible"})
