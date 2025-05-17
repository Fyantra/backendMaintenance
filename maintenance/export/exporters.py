from .exports import BaseExporter
from reportlab.lib.units import inch

class EndroitExporter(BaseExporter):
    model_name = 'Endroit'
    columns = {
        'nom_endroit': 'Nom',
        'date_creation': 'Date de création'
    }
    excluded_fields = ['deleted_at']  # On garde date_creation
    title = 'endroits'
    
class ResponsableExporter(BaseExporter):
    model_name = 'Responsable'
    columns = {
        'nom_responsable': 'Nom',
        'email': 'Email',
        'telephone': 'Téléphone',
        'photo': 'Photo',
        'date_creation': 'Date de création'
    }
    title = 'responsables'

class AtelierExporter(BaseExporter):
    model_name = 'Atelier'
    columns = {
        'nom_atelier': 'Nom de l\'atelier',
        'endroit': 'Endroit',
        'responsable': 'Responsable',
        'date_creation': 'Date de création'
    }
    title = 'ateliers'
    
class ChaineExporter(BaseExporter):
    model_name = 'Chaine'
    columns = {
        'nom_chaine': 'Chaine',
        'atelier': 'Atelier',
        'date_creation': 'Date de création'
    }
    title = 'chaines'

class ModeleExporter(BaseExporter):
    model_name = 'Modele'
    columns = {
        'nom_modele': 'Nom',
        'date_creation': 'Date de création'
    }
    title = 'modèles'

class TypeExporter(BaseExporter):
    model_name = 'Type'
    columns = {
        'nom_type': 'Nom',
        'date_creation': 'Date de création'
    }
    title = 'types'

class MarqueExporter(BaseExporter):
    model_name = 'Marque'
    columns = {
        'nom_marque': 'Nom',
        'date_creation': 'Date de création'
    }
    title = 'marques'
    
class FournisseurExporter(BaseExporter):
    model_name = 'Fournisseur'
    columns = {
        'nom_fournisseur': 'Nom du fournisseur',
        'email': 'Email',
        'telephone': 'Téléphone',
        'date_creation': 'Date de création'
    }
    title = 'fournisseurs'

class MachineExporter(BaseExporter):
    model_name = 'Machine'
    columns = {
        'numero_machine' : 'N°',
        'nom_machine': 'Nom de la machine',
        'image': 'Image',
        'numero_de_serie': 'Numéro de série',
        'atelier' : 'Atelier',
        'chaine' : 'Chaine',
        'modele' : "Modèle",
        'type' : "Type",
        'date_acquisition': 'Date d\'acquisition',
        'date_creation': 'Date de création'
    }
    
    pagesize = (11*inch, 17*inch)
    title = 'machines'
    # date_format = "%A %d %B %Y"  # Format: "Lundi 01 janvier 2024"
    # datetime_format = "%d/%m/%Y à %H:%M"  # Format: "Lundi 01 janvier 2024 à 14h30"
        
class PieceDetacheeExporter(BaseExporter):
    model_name = 'PieceDetachee'
    columns = {
        'nom_piecedetache': 'Nom',
        'image' : 'Image',
        'description': 'Description',
        'prix_unitaire': 'Prix unitaire',
        'quantite': 'Quantité',
        'emplacement': 'Emplacement',
        'stock_min': 'Stock minimum',
        'stock_max': 'Stock maximum',
        'fournisseur': 'Fournisseur',
        'date_creation': 'Date de création'
    }
    
    pagesize = (11*inch, 17*inch)
    title = 'pièces détachées'