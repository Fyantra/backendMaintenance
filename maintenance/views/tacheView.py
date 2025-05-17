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
