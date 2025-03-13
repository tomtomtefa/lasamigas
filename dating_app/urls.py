from django.urls import re_path
from chat import routing  # 🔹 Import du fichier routing.py de l'app chat
from django.conf.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),  
    path("api/chat/", include("chat.urls")),
    path("", chat_room, name="home"),

    # 🔹 Ajoute cette ligne pour gérer les WebSockets
    re_path(r"ws/chat/$", include(routing.websocket_urlpatterns)),  
]

# 🔹 Gestion des fichiers statiques en mode DEBUG
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
