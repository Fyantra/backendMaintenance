from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Notification, UserNotification
from ..serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

#####################################CRUD#####################################
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(utilisateurs=user).order_by('-date_creation')
    
    @action(detail=True, methods=['post'], url_path='marquer-vue')
    def marquer_vue(self, request, pk=None):
        try:
            notification = self.get_object()
            user_notification = UserNotification.objects.get(user=request.user, notification=notification)
            user_notification.vue = True
            user_notification.save()
            return Response({'status': 'notification vue'})
        except UserNotification.DoesNotExist:
            raise NotFound('Relation UserNotification introuvable pour cet utilisateur et cette notification')

    
#####################################FIN CRUD#####################################
