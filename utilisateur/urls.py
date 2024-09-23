from django.urls import path, include
from rest_framework.routers import DefaultRouter
from utilisateur.views import UtilisateurViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UtilisateurViewSet)

urlpatterns = [
    path('maintenance_api/', include(router.urls)),
    path('maintenance_api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    #pour obtenir le token
    path('maintenance_api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
