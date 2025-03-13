from django.contrib import admin
from django.urls import path, include
from chat.views import chat_room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # 🔹 Vérifie bien cette ligne !
    path('api/chat/', include('chat.urls')),
    path('', chat_room, name='home'),
]

# 🔹 Ajout des fichiers statiques/media en mode DEBUG
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
