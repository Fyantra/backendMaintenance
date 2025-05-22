from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Tache, MotifTache, StatusTache, HistoriqueTache, ActiviteTache, ActiviteTachePieceDetachee
from ..serializers import (TacheSerializer, MotifTacheSerializer, StatusTacheSerializer, HistoriqueTacheSerializer, 
    ActiviteTacheSerializer, ActiviteTachePieceDetacheeSerializer, DocumentSerializer)
from utilisateur.permissions import IsChef
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import Document
from ..services.email_service import send_maintenance_email


#####################################CRUD#####################################
class BaseModelViewSet(viewsets.ModelViewSet):
    

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True).order_by('-date_creation')

    def perform_destroy(self, instance):
       
        instance.deleted_at = now()
        instance.save()

    def get_permissions(self):      #seuls un Chef pour faire les operations CRUD
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsChef]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
class TableFilsViewSet(viewsets.ModelViewSet):
    def get_permissions(self):      
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsChef]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

# Créer les ViewSets pour chaque modèle
class TacheViewSet(BaseModelViewSet):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Envoi des emails si demandé
        if instance.envoyer_email and instance.responsables.exists():
            # Récupérer les emails valides des responsables
            responsables_emails = [
                r.email for r in instance.responsables.all() 
                if r.email and '@' in r.email
            ]
            
            if responsables_emails:
                context = {
                    'tache': instance,
                    'title': "Nouvelle tâche de maintenance",
                    'company_name': "Akanjo Madagascar"
                }
                
                subject = f"Nouvelle tâche de maintenance - {instance.machine.nom_machine}"
                send_maintenance_email(
                    subject=subject,
                    to_emails=responsables_emails,
                    context=context
                )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        previous_responsables = set(instance.responsables.all())  # Responsables avant modification

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Vérifier si l'envoi d'email est demandé
        envoyer_email = request.data.get('envoyer_email', False)
        
        if envoyer_email and instance.responsables.exists():
            current_responsables = set(instance.responsables.all())
            
            # Identifier nouveaux vs anciens responsables
            new_responsables = current_responsables - previous_responsables
            existing_responsables = current_responsables & previous_responsables
            
            # Préparer les listes d'emails
            new_emails = [r.email for r in new_responsables if r.email]
            existing_emails = [r.email for r in existing_responsables if r.email]

            # Envoyer aux nouveaux responsables
            if new_emails:
                send_maintenance_email(
                    subject=f"Nouvelle tâche de maintenance - {instance.machine.nom_machine}",
                    to_emails=new_emails,
                    context={
                        'tache': instance,
                        'title': "Nouvelle tâche de maintenance",
                        'company_name': "Akanjo Madagascar",
                    },
                )
            
            # Envoyer aux anciens responsables
            if existing_emails:
                send_maintenance_email(
                    subject=f"[MISE À JOUR] Modification tâche - {instance.machine.nom_machine}",
                    to_emails=existing_emails,
                    context={
                        'tache': instance,
                        'title' : "Mise à jour de tâche",
                        'company_name': "Akanjo Madagascar", 
                    },
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=['post'], url_path='add_document')
    def add_document(self, request, pk=None):
        tache = self.get_object()
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            document = serializer.save()
            tache.documents.add(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='list_documents')
    def get_documents(self, request, pk=None):
        tache = self.get_object()
        documents = tache.documents.all()
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete_document/(?P<document_id>\d+)')
    def remove_document(self, request, pk=None, document_id=None):
        tache = self.get_object()
        try:
            document = tache.documents.get(id=document_id)
            tache.documents.remove(document)
            document.delete()  # Supprime aussi le fichier physique
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document non trouvé"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
class MotifTacheViewSet(BaseModelViewSet):
    queryset = MotifTache.objects.all()
    serializer_class = MotifTacheSerializer

class StatusTacheViewSet(BaseModelViewSet):
    queryset = StatusTache.objects.all()
    serializer_class = StatusTacheSerializer
    
class HistoriqueTacheViewSet(TableFilsViewSet):
    queryset = HistoriqueTache.objects.all()
    serializer_class = HistoriqueTacheSerializer

class ActiviteTacheViewSet(BaseModelViewSet):
    queryset = ActiviteTache.objects.all()
    serializer_class = ActiviteTacheSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Supprimer toutes les pièces détachées liées
        ActiviteTachePieceDetachee.objects.filter(activite_tache=instance).delete()
        # Supprimer l'ActiviteTache
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ActiviteTachePieceDetacheeViewSet(TableFilsViewSet):
    queryset = ActiviteTachePieceDetachee.objects.all()
    serializer_class = ActiviteTachePieceDetacheeSerializer
#####################################FIN CRUD#####################################
