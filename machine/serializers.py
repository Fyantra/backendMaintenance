# dans serializers.py
from rest_framework import serializers
from .models import Machine, Modele, Type, NomMachine, Marque
from fournisseur.models import Fournisseur
from piece_detache.models import PieceDetachee

class ModeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modele
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class NomMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomMachine
        fields = '__all__'

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    
    modele_id = serializers.PrimaryKeyRelatedField(queryset=Modele.objects.all(), source='modele', write_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), source='type', write_only=True)
    nom_machine_id = serializers.PrimaryKeyRelatedField(queryset=NomMachine.objects.all(), source='nom_machine', write_only=True)
    marque_id = serializers.PrimaryKeyRelatedField(queryset=Marque.objects.all(), source='marque', write_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True)
    piecedetachee_id = serializers.PrimaryKeyRelatedField(queryset=PieceDetachee.objects.all(), source='pieces_detachees', many=True, write_only=True)
    
    class Meta:
        model = Machine
        fields = '__all__'
        
