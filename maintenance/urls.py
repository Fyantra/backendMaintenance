from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.machineView import *
from .views.atelierView import *
from .views.fournisseurView import *
from .views.piecedetacheeView import *
from .views.tacheView import *
from .views.notificationView import *
from .views.exportView import *

routermachine = DefaultRouter()
routermachine.register(r'machines', MachineViewSet)
routermachine.register(r'machine_relation', MachineRelationViewSet)
routermachine.register(r'modeles', ModeleViewSet)
routermachine.register(r'types', TypeViewSet)
routermachine.register(r'noms_machines', NomMachineViewSet)
routermachine.register(r'marques', MarqueViewSet)
routermachine.register(r'status', StatusViewSet)
routermachine.register(r'historique_machine', HistoriqueMouvementMachineViewSet)

routerTache = DefaultRouter()
routerTache.register(r'taches', TacheViewSet)
routerTache.register(r'motif_taches', MotifTacheViewSet)
routerTache.register(r'status_taches', StatusTacheViewSet)
routerTache.register(r'historique_taches', HistoriqueTacheViewSet)
routerTache.register(r'activites_taches', ActiviteTacheViewSet)
routerTache.register(r'activites_piecedetachees', ActiviteTachePieceDetacheeViewSet)

routerNotification = DefaultRouter()
routerNotification.register(r'notifications', NotificationViewSet)

routerAtelier = DefaultRouter()
routerAtelier.register(r'endroits', EndroitViewSet)
routerAtelier.register(r'responsables', ResponsableViewSet)
routerAtelier.register(r'ateliers', AtelierViewSet)
routerAtelier.register(r'chaines', ChaineViewSet)

routerFournisseur = DefaultRouter()
routerFournisseur.register(r'fournisseurs', FournisseurViewSet)

routerPiece = DefaultRouter()
routerPiece.register(r'piecedetachees', PieceDetacheeViewSet)
routerPiece.register(r'reapprovisionnements', ReapprovisionnementPieceDetacheeViewSet)
routerPiece.register(r'historique_mouvement_pieces', HistoriqueMouvementPieceDetacheeViewSet)

urlpatterns = [
    path('maintenance_api/machine/', include(routermachine.urls)),
    path('maintenance_api/atelier/', include(routerAtelier.urls)),
    path('maintenance_api/fournisseur/', include(routerFournisseur.urls)),
    path('maintenance_api/piece/', include(routerPiece.urls)),
    path('maintenance_api/tache/', include(routerTache.urls)),
    path('maintenance_api/', include(routerNotification.urls)),
    
    #URL Export
    path('maintenance_api/export/<str:model_name>/<str:export_format>/', ExportView.as_view()),
    path('maintenance_api/export-tache/<str:export_format>/', ExportTacheView.as_view()),
    path('maintenance_api/export-tache/<int:pk>/<str:export_format>/', ExportTacheView.as_view()),
]
