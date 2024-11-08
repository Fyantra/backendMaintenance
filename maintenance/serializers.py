from rest_framework import serializers
from .models import *
from .sous_serializers import *
import json

class EndroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endroit
        fields = ['id', 'nom_endroit', 'date_creation']

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ['id', 'nom_responsable', 'email', 'telephone', 'photo' , 'date_creation']

class AtelierSerializer(serializers.ModelSerializer):
    endroit = EndroitSousSerializer(read_only=True)
    responsable = ResponsableSousSerializer(read_only=True)

    endroit_id = serializers.PrimaryKeyRelatedField(
        queryset=Endroit.objects.all(), source='endroit'
    )
    responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=Responsable.objects.all(), source='responsable'
    )

    class Meta:
        model = Atelier
        fields = ['id', 'nom_atelier', 'endroit', 'responsable', 'endroit_id', 'responsable_id', 'date_creation']

class ChaineSerializer(serializers.ModelSerializer):
    atelier = AtelierSousSerializer(read_only=True)
    atelier_id = serializers.PrimaryKeyRelatedField(
        queryset=Atelier.objects.all(), source='atelier'
    ) 
        
    class Meta:
        model = Chaine
        fields = ['id', 'nom_chaine', 'atelier', 'atelier_id' ,'date_creation']

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = ['id', 'nom_fournisseur', 'email', 'telephone', 'date_creation']
    
    def validate_email(self, value):
        if value == '':
            return None  # Remplacer les emails vides par NULL
        return value


class ModeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modele
        fields = ['id', 'nom_modele', 'date_creation']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'nom_type', 'date_creation']

class NomMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomMachine
        fields = ['id', 'nom_machine', 'date_creation']

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = ['id', 'nom_marque', 'date_creation']
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'nom_status', 'couleur' , 'date_creation']

                
class MachineRelationSerializer(serializers.ModelSerializer):
    # machine_liee_nom = serializers.CharField(source='machine_liee.nom_machine', read_only=True)
    machine_liee = MachineSousSerializer(read_only=True)
    machine_liee_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(), source='machine_liee', allow_null=True, required=False
    )

    class Meta:
        model = MachineRelation
        fields = ['id', 'machine_principale' , 'machine_liee_id', 'quantite', 'machine_liee']
        
class MachineSerializer(serializers.ModelSerializer):
    marque = MarqueSousSerializer(read_only=True)
    marque_id = serializers.PrimaryKeyRelatedField(
        queryset=Marque.objects.all(), source='marque', allow_null=True, required=False
    )
    
    type = TypeSousSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), source='type', allow_null=True, required=False
    )
    
    status = StatusSousSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source='status'
    )
    
    atelier = AtelierSousSerializer(read_only=True)
    atelier_id = serializers.PrimaryKeyRelatedField(
        queryset=Atelier.objects.all(), source='atelier', allow_null=True, required=False
    )
    
    chaine = ChaineSousSerializer(read_only=True)
    chaine_id = serializers.PrimaryKeyRelatedField(
        queryset=Chaine.objects.all(), source='chaine', allow_null=True, required=False
    )
    
    fournisseur = FournisseurSousSerializer(read_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(
        queryset=Fournisseur.objects.all(), source='fournisseur', allow_null=True, required=False
    )
        
    pieces_detachees = PieceDetacheeSousSerializer(many=True, read_only=True)   #pour les details 
    pieces_detachees_id = serializers.PrimaryKeyRelatedField(
        queryset=PieceDetachee.objects.all(), many=True, source='pieces_detachees', allow_null=True, required= False
    )
    
    class Meta:
        model = Machine
        fields = ['id', 'nom_machine', 'numero_de_serie', 'numero_de_moteur', 'type_id', 'type', 'marque_id', 'marque',  'date_mis_en_place',
                  'date_acquisition','status_id','status', 'atelier_id', 'atelier', 'chaine_id', 'chaine' , 'date_hors_service', 
                  'fournisseur_id', 'fournisseur',  'image', 'description', 'reference_fabricant', 
                  'pieces_detachees_id', 'pieces_detachees' ,  'date_creation']
    
    def create(self, validated_data):
        # Extraire les données pour les pièces détachées
        pieces_detachees_data = validated_data.pop('pieces_detachees', [])
        
        machine = Machine.objects.create(**validated_data)

        # Ajouter les pièces détachées
        machine.pieces_detachees.set(pieces_detachees_data)

        return machine

    def update(self, instance, validated_data):
        pieces_detachees_data = validated_data.pop('pieces_detachees', [])

        # Mettre à jour les autres champs de la machine principale en utilisant validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        instance.pieces_detachees.set(pieces_detachees_data)

        # Supprimer les anciennes relations
        MachineRelation.objects.filter(machine_principale=instance).delete()

        return instance
    

class PieceDetacheeSerializer(serializers.ModelSerializer):
    modele = ModeleSousSerializer(read_only=True)
    emplacement = AtelierSousSerializer(read_only= True)
    fournisseur = FournisseurSousSerializer(read_only=True)
    
    modele_id = serializers.PrimaryKeyRelatedField(
        queryset=Modele.objects.all(), source='modele', allow_null=True, required=False
    )
    
    emplacement_id = serializers.PrimaryKeyRelatedField(
        queryset=Atelier.objects.all(), source='emplacement', allow_null=True, required=False
    ) 
    
    fournisseur_id = serializers.PrimaryKeyRelatedField(
        queryset=Fournisseur.objects.all(), source='fournisseur', allow_null=True, required=False
    ) 
    
    class Meta:
        model = PieceDetachee
        fields = ['id', 'nom_piecedetache', 'description', 'modele', 'date_achat', 'prix_unitaire', 'quantite', 'emplacement', 'fournisseur',
                  'modele_id', 'emplacement_id', 'fournisseur_id','reference_fabricant', 'image', 'stock_min', 'stock_max', 
                  'lot_de_reapprovisionnement', 'date_creation']


class HistoriqueMouvementMachineSerializer(serializers.ModelSerializer):
    machine = MachineSousSerializer(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(), source='machine'
    )
    
    atelier = AtelierSousSerializer(read_only=True)
    atelier_id = serializers.PrimaryKeyRelatedField(
        queryset=Atelier.objects.all(), source='atelier'
    )
    
    chaine = ChaineSousSerializer(read_only=True)
    chaine_id = serializers.PrimaryKeyRelatedField(
        queryset=Chaine.objects.all(), source='chaine'
    )
    
    class Meta:
        model = HistoriqueMouvementMachine
        fields = ['id', 'machine_id', 'machine', 'atelier_id', 'atelier', 'chaine_id', 'chaine' , 'date_creation']