from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(UserAdmin):  # On utilise le modèle UserAdmin pour les utilisateurs
    fieldsets = UserAdmin.fieldsets + (  # Ajoute nos champs personnalisés
        ('Informations supplémentaires', {'fields': ('bio', 'photo', 'age', 'location')}),
    )

admin.site.register(UserProfile, UserProfileAdmin)  # On enregistre notre modèle dans l'admin
