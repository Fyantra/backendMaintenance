from rest_framework.views import APIView
from django.http import Http404
from ..export.utils import get_exporter_class  
from ..export.exports import TacheExporter

class ExportView(APIView):
    def get(self, request, model_name, export_format):
        try:
            exporter_class = get_exporter_class(model_name)
            if export_format == 'pdf':
                return exporter_class.export_pdf(request)
            elif export_format == 'csv':
                return exporter_class.export_csv(request)
            elif export_format == 'excel':
                return exporter_class.export_excel(request)
            raise Http404("Format d'export non supporté")
        except ValueError as e:
            raise Http404(str(e))
        
class ExportTacheView(APIView):
    def get(self, request, export_format, pk=None):
        try:
            if export_format == 'pdf':
                return TacheExporter.export_pdf(request, pk)
            elif export_format == 'excel':
                return TacheExporter.export_excel(request)
            elif export_format == 'csv':
                return TacheExporter.export_csv(request)
            raise Http404("Format d'export de tache non supporté")
        except ValueError as e:
            raise Http404(str(e))
