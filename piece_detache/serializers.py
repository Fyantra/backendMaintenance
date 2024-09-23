from rest_framework import serializers
from .models import PieceDetachee
from machine.models import Modele
from atelier.models import Atelier
from fournisseur.models import Fournisseur

class PieceDetacheeSerializer(serializers.ModelSerializer):
    
    modele_id = serializers.PrimaryKeyRelatedField(queryset=Modele.objects.all(), source='modele', write_only=True)
    emplacement_id = serializers.PrimaryKeyRelatedField(queryset=Atelier.objects.all(), source='emplacement', write_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True)
    
    class Meta:
        model = PieceDetachee
        fields = '__all__'
