from django import forms
from .models import Kuliner, Penginapan, Wisata, CustomUser
from django.contrib.auth.forms import UserCreationForm


# Form untuk Kuliner
class KulinerForm(forms.ModelForm):
    class Meta:
        model = Kuliner
        fields = ['nama', 'deskripsi', 'google_maps_url', 'foto']


# Form untuk Penginapan
class PenginapanForm(forms.ModelForm):
    class Meta:
        model = Penginapan
        fields = ['nama', 'deskripsi', 'google_maps_url', 'foto']


# Form untuk Wisata
class WisataForm(forms.ModelForm):
    class Meta:
        model = Wisata
        fields = ['nama', 'deskripsi', 'google_maps_url', 'foto']


# Form untuk Signup dengan pilihan Role
class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'contributor'  # Tetapkan role menjadi contributor
        if commit:
            user.save()
        return user
