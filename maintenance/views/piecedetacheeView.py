from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utilisateur.permissions import IsChef
from ..models import PieceDetachee, ReapprovisionnementPieceDetachee, HistoriqueMouvementPieceDetachee
from ..serializers import PieceDetacheeSerializer, ReapprovisionnementPieceDetacheeSerializer, HistoriqueMouvementPieceDetacheeSerializer
from django.utils import timezone

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

class ReapprovisionnementPieceDetacheeViewSet(BaseModelViewSet):
    queryset = ReapprovisionnementPieceDetachee.objects.all()
    serializer_class = ReapprovisionnementPieceDetacheeSerializer    

class HistoriqueMouvementPieceDetacheeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoriqueMouvementPieceDetachee.objects.all()
    serializer_class = HistoriqueMouvementPieceDetacheeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HistoriqueMouvementPieceDetachee.objects.order_by('-date_creation')