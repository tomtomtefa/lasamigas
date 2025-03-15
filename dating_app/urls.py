from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),  # ✅ Inclure toutes les URLs de `chat`
]
