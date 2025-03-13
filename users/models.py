from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


# 🔹 Modèle pour gérer les Likes
class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="likes_given")
    liked_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="likes_received")
    timestamp = models.DateTimeField(auto_now_add=True)  # Date du like

    class Meta:
        unique_together = ('user', 'liked_user')  # Un utilisateur ne peut liker un autre qu'une seule fois
        verbose_name_plural = "Likes"  # Nom plus propre dans l'admin

    def __str__(self):
        return f"{self.user} → ❤️ → {self.liked_user}"

    def clean(self):
        """ Empêche un utilisateur de liker son propre profil """
        if self.user == self.liked_user:
            raise ValidationError("❌ Impossible de liker son propre profil.")

    def save(self, *args, **kwargs):
        """ Vérification avant sauvegarde """
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def has_liked(cls, user, liked_user):
        """ Vérifie si un utilisateur a déjà liké un autre """
        return cls.objects.filter(user=user, liked_user=liked_user).exists()
