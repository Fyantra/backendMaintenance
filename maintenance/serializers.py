from rest_framework import serializers
from .models import *

class EndroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endroit
        fields = ['id', 'nom_endroit', 'date_creation']


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ['id', 'nom_responsable', 'email', 'telephone', 'photo' , 'date_creation']


class AtelierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Atelier
        fields = '__all__'


class ChaineSerializer(serializers.ModelSerializer):
        
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
    
    class Meta:
        model = Machine
        fields = '__all__'
        
        
class PieceDetacheeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PieceDetachee
        fields = '__all__'
