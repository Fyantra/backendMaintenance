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
        fields = ['id', 'nom_responsable', 'responsabilite' ,'email', 'telephone', 'photo' , 'date_creation']

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
        fields = ['id', 'nom_status', 'couleur' , 'identifiant', 'date_creation']

                
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
    
    modele = ModeleSousSerializer(read_only=True)
    modele_id = serializers.PrimaryKeyRelatedField(
        queryset=Modele.objects.all(), source='modele', allow_null=True, required=False
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
    
    total_duree_machine = serializers.SerializerMethodField()       ##temps total passe sur le machine
    total_duree_machine_liee = serializers.SerializerMethodField()
    
    class Meta:
        model = Machine
        fields = ['id', 'numero_machine', 'nom_machine', 'numero_de_serie', 'numero_de_moteur', 'type_id', 'type', 'marque_id', 'marque', 'modele_id', 'modele', 
                  'date_mis_en_place','date_acquisition','identifiant_status_machine', 'atelier_id', 'atelier', 'chaine_id', 'chaine' , 'date_hors_service', 
                  'fournisseur_id', 'fournisseur',  'image', 'description', 'reference_fabricant', 
                  'pieces_detachees_id', 'pieces_detachees' , 'total_duree_machine', 'total_duree_machine_liee', 'date_creation']
    
    def create(self, validated_data):
        # Extraire les données pour les pièces détachées
        pieces_detachees_data = validated_data.pop('pieces_detachees', [])
        
        # Formater le numero_machine
        numero_machine = validated_data.get('numero_machine')
        if numero_machine and len(numero_machine) < 4:
            validated_data['numero_machine'] = numero_machine.zfill(4)
        
        machine = Machine.objects.create(**validated_data)

        # Ajouter les pièces détachées
        machine.pieces_detachees.set(pieces_detachees_data)

        return machine

    def update(self, instance, validated_data):
        pieces_detachees_data = validated_data.pop('pieces_detachees', [])
        
        numero_machine = validated_data.get('numero_machine')
        if numero_machine and len(numero_machine) < 4:
            validated_data['numero_machine'] = numero_machine.zfill(4)

        # Mettre à jour les autres champs de la machine principale en utilisant validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        instance.pieces_detachees.set(pieces_detachees_data)

        # Supprimer les anciennes relations
        MachineRelation.objects.filter(machine_principale=instance).delete()

        return instance
    
    def get_total_duree_machine(self, obj):
        """Calcule la durée totale des tâches associées à une machine."""
        taches = Tache.objects.filter(machine=obj)
        activites = ActiviteTache.objects.filter(tache__in=taches, deleted_at__isnull=True)

        total_heures = sum(activite.temps_passe_heure or 0 for activite in activites)
        total_minutes = sum(activite.temps_passe_minute or 0 for activite in activites)

        total_heures += total_minutes // 60
        total_minutes = total_minutes % 60

        return f"{total_heures}h {total_minutes}mn"
    
    def get_total_duree_machine_liee(self, obj):
        """Calcule la durée totale des tâches associées aux machines liées à une machine principale."""
        
        # Machine principale incluse
        machines_a_inclure = [obj]
        
        machines_liees = Machine.objects.filter(machine_liee__machine_principale=obj)
        machines_a_inclure += list(machines_liees)

        taches = Tache.objects.filter(machine__in=machines_a_inclure, deleted_at__isnull=True)

        activites = ActiviteTache.objects.filter(tache__in=taches, deleted_at__isnull=True)

        total_heures = sum(activite.temps_passe_heure or 0 for activite in activites)
        total_minutes = sum(activite.temps_passe_minute or 0 for activite in activites)

        total_heures += total_minutes // 60
        total_minutes = total_minutes % 60

        return f"{total_heures}h {total_minutes}mn"

    
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
        
    def create(self, validated_data):
        # Création de la pièce détachée
        piece_detachee = super().create(validated_data)

        # Enregistrement dans l'historique des mouvements
        HistoriqueMouvementPieceDetachee.objects.create(
            piece_detachee=piece_detachee,
            source='Inventaire',
            date_realisation=piece_detachee.date_creation,  # Utilisation de la date de création de l'instance
            quantite=0,
            cout=0,
            quantite_piece=piece_detachee.quantite  # Quantité actuelle après insertion
        )

        return piece_detachee


class HistoriqueMouvementMachineSerializer(serializers.ModelSerializer):
    machine = HistoriqueDeplacementMachineSousSerializer(read_only=True)
    
    atelier = AtelierSousSerializer(read_only=True)
    
    chaine = ChaineSousSerializer(read_only=True)
    
    class Meta:
        model = HistoriqueMouvementMachine
        fields = ['id', 'machine', 'atelier', 'chaine' , 'date_deplacement', 'date_creation']
        

#################################TACHE#########################################
class MotifTacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotifTache
        fields = ['id', 'nom_motif_tache', 'date_creation']
        
class StatusTacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTache
        fields = ['id', 'nom_status_tache', 'couleur', 'identifiant', 'date_creation']
        
class TacheSerializer(serializers.ModelSerializer):
    machine = MachineSousSerializer(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(), source='machine'
    )
    
    motif_tache = MotifTacheSousSerializer(read_only=True)
    motif_tache_id = serializers.PrimaryKeyRelatedField(
        queryset=MotifTache.objects.all(), source='motif_tache', allow_null=True, required=False
    )
     
    total_duree_tache = serializers.SerializerMethodField() 
        
    class Meta:
        model = Tache
        fields = ['id', 'description', 'machine', 'machine_id', 'motif_tache', 'motif_tache_id', 'identifiant_status_tache',
                  'date_debut', 'heure_debut', 'date_fin', 'heure_fin', 'temps_maintenance_heure', 'temps_maintenance_minute',
                  'temps_arret_heure', 'temps_arret_minute', 'total_duree_tache', 'date_creation']
        
    def get_total_duree_tache(self, obj):
        """Calcule la durée totale de toutes les activités liées à une tâche."""
        activites = ActiviteTache.objects.filter(tache=obj, deleted_at__isnull=True)

        # Somme des heures et minutes
        total_heures = sum(activite.temps_passe_heure or 0 for activite in activites)
        total_minutes = sum(activite.temps_passe_minute or 0 for activite in activites)

        # Conversion des minutes en heures si nécessaire
        total_heures += total_minutes // 60
        total_minutes = total_minutes % 60

        return f"{total_heures}h {total_minutes}mn"
    
class HistoriqueTacheSerializer(serializers.ModelSerializer):
    tache = TacheSerializer(read_only = True)
    
    class Meta:
        model = HistoriqueTache
        fields = ['id', 'tache', 'date_creation']
        
class ActiviteTacheSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ActiviteTache
        fields = ['id', 'description', 'date_realisation', 'temps_passe_heure', 'temps_passe_minute', 'tache', 'date_creation']
        
class ActiviteTachePieceDetacheeSerializer(serializers.ModelSerializer):
    pieces_detachees = PieceDetacheeActiviteSousSerializer(read_only=True)
    pieces_detachees_id = serializers.PrimaryKeyRelatedField(
        queryset=PieceDetachee.objects.all(), source='pieces_detachees', allow_null=True, required=False
    )
    
    total = serializers.SerializerMethodField()

    # Champ calculé pour le total de tous les ActiviteTachePieceDetachee liés à la même activité
    somme_totale = serializers.SerializerMethodField()
    
    class Meta:
        model = ActiviteTachePieceDetachee
        fields = ['id', 'activite_tache', 'pieces_detachees_id', 'pieces_detachees', 'quantite', 'prix_piece_detachees','total', 'somme_totale']
            
    def create(self, validated_data):
        piece_detachee = validated_data.get('pieces_detachees')
        quantite_demandee = validated_data.get('quantite')
        prix_piece = piece_detachee.prix_unitaire

        if quantite_demandee > piece_detachee.quantite:
            raise serializers.ValidationError({
                "quantite": f"La quantité demandée ({quantite_demandee}) dépasse la quantité disponible ({piece_detachee.quantite})."
            })

        validated_data['prix_piece_detachees'] = prix_piece
        # Mise à jour de la quantité de la pièce détachée
        piece_detachee.quantite -= quantite_demandee
        piece_detachee.save()

        # Calcul du coût total
        cout = quantite_demandee * prix_piece

        # Enregistrement dans l'historique des mouvements
        HistoriqueMouvementPieceDetachee.objects.create(
            piece_detachee=piece_detachee,
            tache = validated_data.get('activite_tache').tache,
            source='Consommation',
            date_realisation=validated_data.get('activite_tache').date_realisation,
            quantite=-quantite_demandee,        #negatif car c`est un consommation`
            cout=cout,
            quantite_piece=piece_detachee.quantite  # Quantité actuelle après consommation
        )

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        piece_detachee = validated_data.get('pieces_detachees', instance.pieces_detachees)
        nouvelle_quantite = validated_data.get('quantite', instance.quantite)

        if piece_detachee:
            # Restaurer la quantité précédente dans la pièce détachée
            piece_detachee.quantite += instance.quantite

            # Valider la nouvelle quantité
            if nouvelle_quantite > piece_detachee.quantite:
                raise serializers.ValidationError({
                    "quantite": f"La nouvelle quantité ({nouvelle_quantite}) dépasse la quantité disponible ({piece_detachee.quantite})."
                })

            piece_detachee.quantite -= nouvelle_quantite
            piece_detachee.save()

        return super().update(instance, validated_data)

    def get_total(self, obj):
        """Calcule le total pour un objet spécifique."""
        if obj.quantite is not None and obj.prix_piece_detachees is not None:
            return obj.quantite * obj.prix_piece_detachees
        return 0

    def get_somme_totale(self, obj):
        """Calcule la somme totale pour tous les objets liés à la même activité."""
        if obj.activite_tache:
            # Récupérer tous les objets liés à l'activité
            activite_pieces = ActiviteTachePieceDetachee.objects.filter(activite_tache=obj.activite_tache)

            # Calculer la somme totale
            return sum(
                (piece.quantite or 0) * (piece.prix_piece_detachees or 0)
                for piece in activite_pieces
            )
        return 0
    
    
class NotificationSerializer(serializers.ModelSerializer):
    vue = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'piece_detachee', 'date_creation', 'vue']

    def get_vue(self, obj):
        user = self.context['request'].user
        try:
            user_notification = UserNotification.objects.get(user=user, notification=obj)
            return user_notification.vue
        except UserNotification.DoesNotExist:
            return False
        
class ReapprovisionnementPieceDetacheeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReapprovisionnementPieceDetachee
        fields = ['id', 'pieces_detachees', 'prix_piece_detachees', 'quantite', 'date_realisation', 'date_creation']
    
    def create(self, validated_data):
        piece_detachee = validated_data['pieces_detachees']
        prix_piece_detachees = validated_data.get('prix_piece_detachees', piece_detachee.prix_unitaire)

        if prix_piece_detachees != piece_detachee.prix_unitaire:
            piece_detachee.prix_unitaire = prix_piece_detachees
            piece_detachee.save()

        validated_data['prix_piece_detachees'] = prix_piece_detachees

        quantite_reapprovisionnee = validated_data['quantite']
        piece_detachee.quantite += quantite_reapprovisionnee
        piece_detachee.save()

        cout_reapprovisionnement = quantite_reapprovisionnee * prix_piece_detachees

        # Ajout dans l'historique des mouvements
        HistoriqueMouvementPieceDetachee.objects.create(
            piece_detachee=piece_detachee,
            source='Réapprovisionnement',
            date_realisation=validated_data['date_realisation'],
            quantite=quantite_reapprovisionnee,
            cout=cout_reapprovisionnement,
            quantite_piece=piece_detachee.quantite  # Quantité actuelle après réapprovisionnement
        )

        return super().create(validated_data)


class HistoriqueMouvementPieceDetacheeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueMouvementPieceDetachee
        fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'document_type', 'file', 'link', 
            'description', 'created_at', 'file_url', 'file_size'
        ]
        read_only_fields = ['created_at', 'file_url', 'file_size']

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None

    def validate(self, data):
        if data.get('document_type') == 'file' and not data.get('file'):
            raise serializers.ValidationError("Un fichier est requis pour ce type de document.")
        if data.get('document_type') == 'link' and not data.get('link'):
            raise serializers.ValidationError("Un lien est requis pour ce type de document.")
        return data