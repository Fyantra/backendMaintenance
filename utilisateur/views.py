# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny    #AllowAny: tous le monde peut acceder
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
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

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)   #Crée un jeton de rafraîchissement pour l'utilisateur
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            response = Response({
                'message': 'Login successful',
                'user': UtilisateurSerializer(user).data,  # Ajoutez les informations de l'utilisateur
                'access': str(access_token),
                'refresh': str(refresh),
            })

            # Stocker les tokens dans des cookies HttpOnly
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                samesite='Lax',
                secure=True
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=True
            )

            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                access_token = refresh.access_token

                response = Response({'message': 'Token refreshed successfully'})
                response.set_cookie(
                    key='access_token',
                    value=str(access_token),
                    httponly=True,
                    samesite='Lax',
                    secure=True
                )
                return response
            except Exception:
                return Response({'error': 'Invalid refresh token'}, status=401)
        return Response({'error': 'No refresh token provided'}, status=400)