from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utilisateur.permissions import IsChef
from .models import Endroit, Responsable, Atelier, Chaine
from .serializers import EndroitSerializer, ResponsableSerializer, AtelierSerializer, ChaineSerializer
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

class EndroitViewSet(BaseModelViewSet):
    queryset = Endroit.objects.filter(deleted_at__isnull=True)
    serializer_class = EndroitSerializer


class ResponsableViewSet(BaseModelViewSet):
    queryset = Responsable.objects.filter(deleted_at__isnull=True)
    serializer_class = ResponsableSerializer


class AtelierViewSet(BaseModelViewSet):
    queryset = Atelier.objects.filter(deleted_at__isnull=True)
    serializer_class = AtelierSerializer


class ChaineViewSet(BaseModelViewSet):
    queryset = Chaine.objects.filter(deleted_at__isnull=True)
    serializer_class = ChaineSerializer
    
#####################################FIN CRUD#####################################
