from rest_framework import serializers
from .models import *

# Sérialiseur allégé 
class MereSousSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Si deleted_at n'est pas null, retournez un dictionnaire vide
        if instance.deleted_at:
            return {}
        return super().to_representation(instance)
    
class EndroitSousSerializer(MereSousSerializer):
    class Meta:
        model = Endroit
        fields = ['id','nom_endroit']

class ResponsableSousSerializer(MereSousSerializer):
    class Meta:
        model = Responsable
        fields = ['id','nom_responsable']
        
class AtelierSousSerializer(MereSousSerializer):
    class Meta:
        model = Atelier
        fields = ['id','nom_atelier']  

class ChaineSousSerializer(MereSousSerializer):
    class Meta:
        model = Chaine
        fields = ['id','nom_chaine']

class FournisseurSousSerializer(MereSousSerializer):
    class Meta:
        model = Fournisseur
        fields = ['id','nom_fournisseur']  

class ModeleSousSerializer(MereSousSerializer):
    class Meta:
        model = Modele
        fields = ['id','nom_modele']  

class TypeSousSerializer(MereSousSerializer):
    class Meta:
        model = Type
        fields = ['id','nom_type']

class MarqueSousSerializer(MereSousSerializer):
    class Meta:
        model = Marque
        fields = ['id','nom_marque']
        
class StatusSousSerializer(MereSousSerializer):
    class Meta:
        model = Status
        fields = ['id','nom_status']


class MachineSousSerializer(MereSousSerializer):
    
    class Meta:
        model = Machine
        fields = ['id','nom_machine', 'numero_de_serie' ,'image']
        
# class MachineRelationSousSerializer(MereSousSerializer):
#     class Meta:
#         model = MachineRelation
#         fields = ['machine_liee', 'quantite']
        
class PieceDetacheeSousSerializer(MereSousSerializer):
    modele = ModeleSousSerializer(read_only=True)
    emplacement = AtelierSousSerializer(read_only=True)
    
    class Meta:
        model = PieceDetachee
        fields = ['id','nom_piecedetache', 'modele' ,'prix_unitaire', 'quantite', 'emplacement','image']