from django.db import models
from atelier.models import Atelier
from fournisseur.models import Fournisseur
# from machine.models import Modele
    
# Create your models here.

class PieceDetachee(models.Model):
    nom_piecedetache = models.CharField(max_length=100, null=False, verbose_name="Nom de la pièce détachée")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    modele = models.ForeignKey('machine.Modele', on_delete=models.SET_NULL,null=True,verbose_name="Modele")
    date_achat = models.DateField(null=True, blank=True, verbose_name="Date d'achat")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Prix unitaire")
    emplacement = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Emplacement")      #emplacement du piece detache
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    image = models.ImageField(upload_to='piece_detaches',null=False, verbose_name="Image")
    stock_min = models.PositiveIntegerField(null=False, verbose_name="Stock minimum")
    stock_max = models.PositiveIntegerField(null=False, verbose_name="Stock maximum")
    lot_de_reapprovisionnement = models.PositiveSmallIntegerField(null=False, verbose_name="Lot de réapprovisionnement")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_piecedetache