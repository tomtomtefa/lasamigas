from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .models import UserProfile, Like
from .serializers import UserProfileSerializer
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm


# 🔹 Vue classique pour afficher la liste des utilisateurs (HTML)
def user_list_page(request):
    users = UserProfile.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


# 🔹 Vue API DRF pour récupérer tous les utilisateurs
class UserProfileListCreate(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# 🔹 Vue API DRF pour un utilisateur spécifique
class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# 🔹 Inscription
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            return redirect('user-profile', username=user.username)  # Redirection vers le profil
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


# 🔹 Connexion
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user-profile', username=user.username)  # Redirection vers profil
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


# 🔹 Déconnexion
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirection vers connexion


# 🔹 Profil utilisateur
@login_required
def user_profile(request, username):
    """
    Affiche le profil d'un utilisateur spécifique.
    """
    user = get_object_or_404(UserProfile, username=username)
    liked = Like.objects.filter(user=request.user, liked_user=user).exists()  # Vérifie si l'utilisateur actuel a liké ce profil

    return render(request, 'users/profile.html', {'user': user, 'liked': liked})


# 🔹 Modification du profil utilisateur
@login_required
def edit_profile(request, username):
    """
    Permet à l'utilisateur de modifier uniquement son propre profil.
    """
    user = get_object_or_404(UserProfile, username=username)

    if request.user != user:
        raise PermissionDenied("❌ Vous ne pouvez modifier que votre propre profil.")

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', username=user.username)
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})


# 🔹 Liker un utilisateur
class LikeUserView(APIView):
    """
    Permet à un utilisateur authentifié de liker un autre utilisateur.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        liked_user = get_object_or_404(UserProfile, username=username)

        if request.user == liked_user:
            return Response({"error": "❌ Vous ne pouvez pas vous liker vous-même !"}, status=400)

        # Vérifie si le like existe déjà
        like, created = Like.objects.get_or_create(user=request.user, liked_user=liked_user)

        if not created:
            return Response({"error": "⚠️ Vous avez déjà liké cet utilisateur."}, status=400)

        return Response({"message": f"✅ Vous avez liké {liked_user.username} !", "like_id": like.id}, status=201)


# 🔹 Supprimer un like (Unlike)
class UnlikeUserView(APIView):
    """
    Permet à un utilisateur authentifié de retirer un like.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        liked_user = get_object_or_404(UserProfile, username=username)

        like = Like.objects.filter(user=request.user, liked_user=liked_user)
        if not like.exists():
            return Response({"error": "⚠️ Vous n'avez pas encore liké cet utilisateur."}, status=400)

        like.delete()
        return Response({"message": f"❌ Vous avez retiré votre like de {liked_user.username}."}, status=200)


# 🔹 Voir les utilisateurs qui vous ont liké
class LikedUsersListView(generics.ListAPIView):
    """
    Liste des utilisateurs qui ont liké le profil actuel.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id__in=Like.objects.filter(liked_user=self.request.user).values_list("user", flat=True))


# 🔹 Vue Debug pour voir les utilisateurs en JSON (test)
def debug_info(request):
    return JsonResponse({"message": "Test de debug", "users": list(UserProfile.objects.values())})
