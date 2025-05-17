from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utilisateur.permissions import IsChef
from ..models import PieceDetachee, ReapprovisionnementPieceDetachee, HistoriqueMouvementPieceDetachee
from ..serializers import PieceDetacheeSerializer, ReapprovisionnementPieceDetacheeSerializer, HistoriqueMouvementPieceDetacheeSerializer, DocumentSerializer
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import Document

class BaseModelViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True).order_by('-date_creation')

    def perform_destroy(self, instance):
       
        instance.deleted_at = timezone.now()
        instance.save()

    def get_permissions(self):      #seuls un Chef pour faire les operations CRUD
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsChef]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class PieceDetacheeViewSet(BaseModelViewSet):
    queryset = PieceDetachee.objects.all()
    serializer_class = PieceDetacheeSerializer
    
    @action(detail=True, methods=['post'], url_path='add_document')
    def add_document(self, request, pk=None):
        piece = self.get_object()
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            document = serializer.save()
            piece.documents.add(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='list_documents')
    def get_documents(self, request, pk=None):
        piece = self.get_object()
        documents = piece.documents.all()
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete_document-document/(?P<document_id>\d+)')
    def remove_document(self, request, pk=None, document_id=None):
        piece = self.get_object()
        try:
            document = piece.documents.get(id=document_id)
            piece.documents.remove(document)
            document.delete()  # Supprime aussi le fichier physique
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document non trouvé"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ReapprovisionnementPieceDetacheeViewSet(BaseModelViewSet):
    queryset = ReapprovisionnementPieceDetachee.objects.all()
    serializer_class = ReapprovisionnementPieceDetacheeSerializer    

class HistoriqueMouvementPieceDetacheeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoriqueMouvementPieceDetachee.objects.all()
    serializer_class = HistoriqueMouvementPieceDetacheeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoriqueMouvementPieceDetachee.objects.order_by('-date_creation')