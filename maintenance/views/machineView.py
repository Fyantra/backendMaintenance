from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Machine, Modele, Type, NomMachine, Marque
from ..serializers import MachineSerializer, ModeleSerializer, TypeSerializer, NomMachineSerializer, MarqueSerializer
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

# Créer les ViewSets pour chaque modèle
class MachineViewSet(BaseModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

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

#####################################FIN CRUD#####################################
