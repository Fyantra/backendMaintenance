from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FournisseurViewSet

router = DefaultRouter()
router.register(r'fournisseurs', FournisseurViewSet)

urlpatterns = [
    path('maintenance_api/', include(router.urls)),
]
