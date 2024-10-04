from rest_framework import serializers
from .models import *

class EndroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endroit
        fields = ['id', 'nom_endroit', 'date_creation']


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ['id', 'nom_responsable', 'date_creation']


class AtelierSerializer(serializers.ModelSerializer):
    
    endroit_id = serializers.PrimaryKeyRelatedField(queryset=Endroit.objects.all(), source='endroit', write_only=True)
    responsable_id = serializers.PrimaryKeyRelatedField(queryset=Responsable.objects.all(), source='responsable', write_only=True)
    
    class Meta:
        model = Atelier
        fields = '__all__'


class ChaineSerializer(serializers.ModelSerializer):
    
    atelier_id = serializers.PrimaryKeyRelatedField(queryset=Atelier.objects.all(), source='atelier', write_only=True)
    
    class Meta:
        model = Chaine
        fields = '__all__'

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


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
        fields = ['id', 'nom_machine', 'date_creation']

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
        
        
class PieceDetacheeSerializer(serializers.ModelSerializer):
    
    modele_id = serializers.PrimaryKeyRelatedField(queryset=Modele.objects.all(), source='modele', write_only=True)
    emplacement_id = serializers.PrimaryKeyRelatedField(queryset=Atelier.objects.all(), source='emplacement', write_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True)
    
    class Meta:
        model = PieceDetachee
        fields = '__all__'
