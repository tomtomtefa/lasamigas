from django.urls import path, re_path  # ✅ Ajout de path
from django.contrib import admin
from django.conf.urls import include
from chat import routing  # 🔹 Import du fichier routing.py de l'app chat
from chat.views import chat_room  # ✅ Import de la vue chat_room

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),  
    path("api/chat/", include("chat.urls")),
    path("", chat_room, name="home"),  # ✅ Maintenant Django reconnaît chat_room

    # 🔹 Ajoute cette ligne pour gérer les WebSockets
    re_path(r"ws/chat/", include(routing.websocket_urlpatterns)),  # ❌ Supprime le $
]

# 🔹 Gestion des fichiers statiques en mode DEBUG
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
