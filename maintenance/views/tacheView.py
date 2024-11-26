from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Tache, MotifTache, StatusTache, HistoriqueTache, ActiviteTache, ActiviteTachePieceDetachee
from ..serializers import TacheSerializer, MotifTacheSerializer, StatusTacheSerializer, HistoriqueTacheSerializer, ActiviteTacheSerializer, ActiviteTachePieceDetacheeSerializer
from utilisateur.permissions import IsChef
from django.utils.timezone import now

#####################################CRUD#####################################
class BaseModelViewSet(viewsets.ModelViewSet):
    

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True)

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
