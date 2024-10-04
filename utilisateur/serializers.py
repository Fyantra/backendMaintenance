from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username' , 'first_name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
        }

    def create(self, validated_data):
        user = Utilisateur(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
