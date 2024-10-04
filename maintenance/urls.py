from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.machineView import *
from .views.atelierView import *
from .views.fournisseurView import *
from .views.piecedetacheeView import *

routermachine = DefaultRouter()
routermachine.register(r'machines', MachineViewSet)
routermachine.register(r'modeles', ModeleViewSet)
routermachine.register(r'types', TypeViewSet)
routermachine.register(r'noms_machines', NomMachineViewSet)
routermachine.register(r'marques', MarqueViewSet)

routerAtelier = DefaultRouter()
routerAtelier.register(r'endroits', EndroitViewSet)
routerAtelier.register(r'responsables', ResponsableViewSet)
routerAtelier.register(r'ateliers', AtelierViewSet)
routerAtelier.register(r'chaines', ChaineViewSet)

routerFournisseur = DefaultRouter()
routerFournisseur.register(r'fournisseurs', FournisseurViewSet)

routerPiece = DefaultRouter()
routerPiece.register(r'piecedetachees', PieceDetacheeViewSet)

urlpatterns = [
    path('maintenance_api/machine/', include(routermachine.urls)),
    path('maintenance_api/atelier/', include(routerAtelier.urls)),
    path('maintenance_api/fournisseur/', include(routerFournisseur.urls)),
    path('maintenance_api/piece/', include(routerPiece.urls)),
]
