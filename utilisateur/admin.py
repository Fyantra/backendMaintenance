from django.contrib import admin
from .models import Utilisateur  # Importation de ton modèle

@admin.register(Utilisateur)  # Décorateur pour l'enregistrement du modèle
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')  # Colonnes à afficher dans l'admin
    search_fields = ('username', 'email', 'role')  # Champs sur lesquels la recherche peut être faite
    list_filter = ('role', 'is_active')  # Filtres dans la colonne de droite
    ordering = ('username',)  # Tri des utilisateurs par nom d'utilisateur
