from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Machine, Modele, Type, NomMachine, Marque, Status, MachineRelation, HistoriqueMouvementMachine
from ..serializers import (MachineSerializer, ModeleSerializer, TypeSerializer, NomMachineSerializer, 
    MarqueSerializer, StatusSerializer, MachineRelationSerializer, HistoriqueMouvementMachineSerializer, DocumentSerializer)
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

# Créer les ViewSets pour chaque modèle
class MachineViewSet(BaseModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    
    @action(detail=True, methods=['post'], url_path='add_document')
    def add_document(self, request, pk=None):
        machine = self.get_object()
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            document = serializer.save()
            machine.documents.add(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='list_documents')
    def get_documents(self, request, pk=None):
        machine = self.get_object()
        documents = machine.documents.all()
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete_document/(?P<document_id>\d+)')
    def remove_document(self, request, pk=None, document_id=None):
        machine = self.get_object()
        try:
            document = machine.documents.get(id=document_id)
            machine.documents.remove(document)
            document.delete()  # Supprime aussi le fichier physique
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document non trouvé"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
class MachineRelationViewSet(viewsets.ModelViewSet):
    queryset = MachineRelation.objects.all()
    serializer_class = MachineRelationSerializer
    
    def get_permissions(self):      #seuls un Chef pour faire les operations CRUD
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsChef]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ModeleViewSet(BaseModelViewSet):
    queryset = Modele.objects.all()
    serializer_class = ModeleSerializer

class TypeViewSet(BaseModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class NomMachineViewSet(BaseModelViewSet):
    queryset = NomMachine.objects.all()
    serializer_class = NomMachineSerializer

class MarqueViewSet(BaseModelViewSet):
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    
class StatusViewSet(BaseModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class HistoriqueMouvementMachineViewSet(BaseModelViewSet):
    queryset = HistoriqueMouvementMachine.objects.all()
    serializer_class = HistoriqueMouvementMachineSerializer


#####################################FIN CRUD#####################################
