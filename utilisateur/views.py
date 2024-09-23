# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny    #AllowAny: tous le monde peut acceder
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Utilisateur
from .serializers import UtilisateurSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):        #gerer tous les CRUD utilisateur
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer        #donnee utilisateur en JSON

    def get_permissions(self):
        if self.action == 'create':  # Permet à tout le monde de créer un compte utilisateur
            permission_classes = [AllowAny]
        else:  # Les autres actions nécessitent une authentification
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)   #Crée un jeton de rafraîchissement pour l'utilisateur
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
