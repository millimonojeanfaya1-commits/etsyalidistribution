#!/usr/bin/env python
"""
Script pour créer automatiquement un superutilisateur
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionstock.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Créer un superutilisateur par défaut"""
    username = 'admin'
    email = 'admin@gestionstock.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"L'utilisateur '{username}' existe déjà.")
        user = User.objects.get(username=username)
        print(f"Email: {user.email}")
        print("Vous pouvez vous connecter avec ces identifiants.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superutilisateur cree avec succes!")
        print(f"Nom d'utilisateur: {username}")
        print(f"Email: {email}")
        print(f"Mot de passe: {password}")
        print("\nVous pouvez maintenant vous connecter au systeme:")
        print("http://127.0.0.1:8000/login/")

if __name__ == '__main__':
    create_superuser()
