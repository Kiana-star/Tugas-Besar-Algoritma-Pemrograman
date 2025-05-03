from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.conf import settings  # Import settings to reference custom user model


# Model untuk Custom User
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('contributor', 'Contributor'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='contributor'
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Model untuk Kuliner
class Kuliner(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    google_maps_url = models.URLField(blank=True, null=True)
    foto = models.ImageField(upload_to='kuliner_images/', blank=True, null=True)  # Menyimpan foto kuliner
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

class Penginapan(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    google_maps_url = models.URLField(blank=True, null=True)
    foto = models.ImageField(upload_to='penginapan_images/', blank=True, null=True)  # Menyimpan foto penginapan
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

class Wisata(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    google_maps_url = models.URLField(blank=True, null=True)
    foto = models.ImageField(upload_to='wisata_images/', blank=True, null=True)  # Menyimpan foto wisata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

# Form untuk Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

