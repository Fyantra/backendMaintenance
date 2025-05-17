from rest_framework import viewsets
from ..models import Document
from ..serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_destroy(self, instance):
        # Supprime le fichier physique avant de supprimer l'instance
        if instance.file:
            instance.file.delete()
        instance.delete()

