from django.db import models
from users.models import UserProfile  # On importe les utilisateurs

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()  # Le message envoyé
    timestamp = models.DateTimeField(auto_now_add=True)  # Date et heure d'envoi

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:30]}"
