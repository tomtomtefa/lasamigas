from rest_framework import serializers
from .models import UserProfile, Like

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'photo', 'age', 'location']

# 🔹 Sérialiseur pour gérer les Likes
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'liked_user', 'timestamp']
        read_only_fields = ['user', 'timestamp']
