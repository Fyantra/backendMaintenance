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
        fields = ['id','nom_responsable', 'email', 'photo']
        
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
        fields = ['id','nom_status', 'identifiant', 'couleur']


class MachineSousSerializer(MereSousSerializer):
    type = TypeSousSerializer(read_only=True)
    marque = MarqueSousSerializer(read_only=True)
    atelier = AtelierSousSerializer(read_only=True)
    chaine = ChaineSousSerializer(read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'nom_machine', 'numero_de_serie', 'type', 'marque',  'date_mis_en_place','date_acquisition','identifiant_status_machine', 
                  'atelier', 'chaine' , 'date_hors_service', 'image', 'description','date_creation']

class HistoriqueDeplacementMachineSousSerializer(serializers.ModelSerializer):  #N`herite pas de MereSousSerializer car on veut afficher tous les machines
    type = TypeSousSerializer(read_only=True)
    marque = MarqueSousSerializer(read_only=True)
    atelier = AtelierSousSerializer(read_only=True)
    chaine = ChaineSousSerializer(read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'nom_machine', 'numero_machine', 'numero_de_serie', 'type', 'marque',  'date_mis_en_place','date_acquisition','identifiant_status_machine', 
                  'atelier', 'chaine' , 'date_hors_service', 'image', 'description','date_creation']        
        
class PieceDetacheeSousSerializer(MereSousSerializer):
    modele = ModeleSousSerializer(read_only=True)
    emplacement = AtelierSousSerializer(read_only=True)
    
    class Meta:
        model = PieceDetachee
        fields = ['id','nom_piecedetache', 'modele' ,'prix_unitaire', 'quantite', 'stock_min', 'stock_max', 'emplacement','image']

class PieceDetacheeActiviteSousSerializer(serializers.ModelSerializer):     #pour les pieces detachees dans les activites
    modele = ModeleSousSerializer(read_only=True)
    emplacement = AtelierSousSerializer(read_only=True)
    
    class Meta:
        model = PieceDetachee
        fields = ['id','nom_piecedetache', 'modele' ,'prix_unitaire', 'quantite', 'stock_min', 'stock_max', 'emplacement','image']
        
class MotifTacheSousSerializer(MereSousSerializer):
    class Meta:
        model = MotifTache
        fields = ['id', 'nom_motif_tache']
        
class StatusTacheSousSerializer(MereSousSerializer):
    class Meta:
        model = StatusTache
        fields = ['id', 'nom_status_tache', 'identifiant', 'couleur']
        
