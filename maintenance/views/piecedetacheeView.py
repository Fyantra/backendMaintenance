from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utilisateur.permissions import IsChef
from ..models import PieceDetachee
from ..serializers import PieceDetacheeSerializer
from django.utils import timezone

class PieceDetacheeViewSet(viewsets.ModelViewSet):
    queryset = PieceDetachee.objects.filter(deleted_at__isnull=True)  
    serializer_class = PieceDetacheeSerializer
    
    def get_permissions(self):      
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsChef]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
