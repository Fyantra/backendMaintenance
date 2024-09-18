from django.db import models
from fournisseur.models import Fournisseur
# from piece_detache.models import PieceDetachee

# Create your models here.

class Modele(models.Model):
    nom_modele = models.CharField(max_length=50, unique=True, null=False, verbose_name="Nom du modèle")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_modele
    
    
class Type(models.Model):
    nom_type = models.CharField(max_length=50, null=False, unique=True, verbose_name="Type de machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_type
    
class NomMachine(models.Model):
    nom_machine = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nom de la machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_machine
    

class Marque(models.Model):
    nom_marque = models.CharField(max_length=50, null=False, unique=True, verbose_name="Marque de la machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_marque
    
# class Status(models.Model):
#     nom_status = models.CharField(max_length=50, null=False, unique=True, verbose_name="Statut")
#     date_creation = models.DateTimeField(auto_now_add=True, null=True)
#     deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
#     def __str__(self):
#         return self.nom_status
    
    
class Machine(models.Model):
    STATUT = [
        ('EN_COURS', 'En cours d`utilisation'),
        ('EN_MAINTENANCE', 'En maintenance'),
        ('EN_PANNE', 'En panne'),
        ('HORS_SERVICE', 'Hors service'),
    ]
    
    nom_machine = models.ForeignKey(NomMachine, on_delete=models.SET_NULL,null=True,verbose_name="Nom du machine")
    numero_de_serie = models.CharField(max_length=100, null=False, unique=True, verbose_name="Numero de serie")
    numero_de_moteur = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numero de moteur")
    modele = models.ForeignKey(Modele, on_delete=models.SET_NULL,null=True,verbose_name="Modele")   #ex: PIQUEUSE DOUBLE ETRAINNEMENT JUKI
    type = models.ForeignKey(Type, on_delete=models.SET_NULL,null=True,verbose_name="Type")     #ex: DDL 9000 C 
    marque = models.ForeignKey(Marque, on_delete=models.SET_NULL,null=True,verbose_name="Marque")
    date_mis_en_place = models.DateField(null=True, verbose_name="Date de mise en place")
    status = models.CharField(max_length=20, choices=STATUT, default='HORS_SERVICE', verbose_name="Statut")      #Etat
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    image = models.ImageField(null=False, verbose_name="Image")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    pieces_detachees = models.ManyToManyField('piece_detache.PieceDetachee', blank=True, verbose_name="Pièces détachées")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_machine
    