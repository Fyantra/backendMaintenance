from rest_framework import viewsets
from ..models import Document
from ..serializers import DocumentSerializer
from rest_framework.decorators import action

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()
        if document.file:
            response = FileResponse(document.file.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
            return response
        return Response(status=404)

    def perform_destroy(self, instance):
        # Supprime le fichier physique avant de supprimer l'instance
        if instance.file:
            instance.file.delete()
        instance.delete()

