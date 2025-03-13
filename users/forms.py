from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

# Formulaire d'inscription
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'photo', 'age', 'location']

# Formulaire de connexion
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'photo', 'age', 'location']