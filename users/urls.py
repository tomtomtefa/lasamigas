from django.urls import path
from .views import (
    register, user_login, user_logout, user_profile, edit_profile, user_list_page,
    UserProfileListCreate, UserProfileDetail, debug_info,
    LikeUserView, UnlikeUserView, LikedUsersListView
)

urlpatterns = [
    # 🔹 Authentification & Utilisateurs
    path('register/', register, name='register'),  # Page d'inscription
    path('login/', user_login, name='login'),  # Connexion
    path('logout/', user_logout, name='logout'),  # Déconnexion

    # 🔹 Profil utilisateur
    path('profile/<str:username>/', user_profile, name='user-profile'),  # ✅ Voir un profil
    path('profile/<str:username>/edit/', edit_profile, name='edit-profile'),  # ✅ Modifier son profil

    # 🔹 Liste des utilisateurs
    path('list/', user_list_page, name='user-list-page'),  # Page HTML avec les utilisateurs

    # 🔹 API DRF - Gestion des utilisateurs
    path('api/', UserProfileListCreate.as_view(), name='user-api-list'),  # API JSON pour tous les utilisateurs
    path('api/<int:pk>/', UserProfileDetail.as_view(), name='user-api-detail'),  # API JSON pour un utilisateur spécifique

    # 🔹 Gestion des Likes
    path('like/<str:username>/', LikeUserView.as_view(), name='like-user'),  # Liker un utilisateur
    path('unlike/<str:username>/', UnlikeUserView.as_view(), name='unlike-user'),  # Retirer un like
    path('likes/', LikedUsersListView.as_view(), name='likes-received'),  # Voir qui m'a liké

    # 🔹 Debug (optionnel)
    path('debug/', debug_info, name='debug-info'),  # Voir tous les utilisateurs en JSON (test)
]
