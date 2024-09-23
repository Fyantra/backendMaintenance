from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EndroitViewSet, ResponsableViewSet, AtelierViewSet, ChaineViewSet

router = DefaultRouter()
router.register(r'endroits', EndroitViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'ateliers', AtelierViewSet)
router.register(r'chaines', ChaineViewSet)

urlpatterns = [
    path('maintenance_api/', include(router.urls)),
]
