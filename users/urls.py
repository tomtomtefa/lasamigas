from django.urls import path
from .views import (
    register, user_login, user_logout, user_profile, edit_profile, user_list_page,
    UserProfileListCreate, UserProfileDetail, debug_info,
    LikeUserView, UnlikeUserView, LikedUsersListView
)

urlpatterns = [
    # 🔹 Authentification & Utilisateurs
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # 🔹 Profil utilisateur
    path('profile/<str:username>/', user_profile, name='user-profile'),
    path('profile/<str:username>/edit/', edit_profile, name='edit-profile'),

    # 🔹 Liste des utilisateurs
    path('list/', user_list_page, name='user-list-page'),

    # 🔹 API DRF - Gestion des utilisateurs
    path('api/', UserProfileListCreate.as_view(), name='user-api-list'),
    path('api/<int:pk>/', UserProfileDetail.as_view(), name='user-api-detail'),

    # 🔹 Gestion des Likes
    path('like/<str:username>/', LikeUserView.as_view(), name='like-user'),
    path('unlike/<str:username>/', UnlikeUserView.as_view(), name='unlike-user'),
    path('likes/', LikedUsersListView.as_view(), name='likes-received'),
]
