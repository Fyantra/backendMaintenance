from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PieceDetacheeViewSet

router = DefaultRouter()
router.register(r'piecedetachees', PieceDetacheeViewSet)

urlpatterns = [
    path('maintenance_api/', include(router.urls)),
]
