# dans urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, ModeleViewSet, TypeViewSet, NomMachineViewSet, MarqueViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'modeles', ModeleViewSet)
router.register(r'types', TypeViewSet)
router.register(r'noms_machines', NomMachineViewSet)
router.register(r'marques', MarqueViewSet)

urlpatterns = [
    path('maintenance_api/', include(router.urls)),
]
