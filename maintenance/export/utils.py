from .exporters import *

def get_exporter_class(model_name):
    exporters = {
        'machine': MachineExporter,
        'endroit': EndroitExporter,
        'responsable': ResponsableExporter,
        'atelier': AtelierExporter,
        'chaine': ChaineExporter,
        'modele': ModeleExporter,
        'type': TypeExporter,
        'marque': MarqueExporter,
        'fournisseur': FournisseurExporter,
        'piecedetachee': PieceDetacheeExporter,
    }
    
    exporter_class = exporters.get(model_name.lower())
    if not exporter_class:
        raise ValueError(f"Exporteur non trouvé pour le modèle {model_name}")
    return exporter_class