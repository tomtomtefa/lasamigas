from django.contrib import admin
from django.urls import path, include, re_path
from chat import routing  # ✅ Import du fichier routing.py pour WebSockets
from chat.views import chat_room  # ✅ Import de la vue principale du chat

urlpatterns = [
    # 🔹 Administration Django
    path("admin/", admin.site.urls),

    # 🔹 Routes pour les utilisateurs
    path("api/users/", include("users.urls")),

    # 🔹 Routes pour le chat (correction ici)
    path("chat/", include("chat.urls")),  # ✅ S'assure que /chat/ est bien pris en compte

    # 🔹 Page d'accueil menant au chat général
    path("", chat_room, name="home"),

    # 🔹 Gestion des WebSockets
    re_path(r"ws/chat/", include(routing.websocket_urlpatterns)),  # ✅ Correction ici
]
