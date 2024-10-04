from django.db import models

# Create your models here.
class Endroit(models.Model):        #ex: RDC, R+1, R+2, ....
    nom_endroit = models.CharField(max_length=50, null=False, unique=True, verbose_name="Endroit")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_endroit
    
class Responsable(models.Model):
    nom_responsable = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Téléphone")
    photo = models.ImageField(null=True, verbose_name="Photo")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_responsable
    
class Atelier(models.Model):
    nom_atelier = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nom d`atelier")
    endroit = models.ForeignKey(Endroit, null=True,on_delete=models.SET_NULL, verbose_name="Endroit")
    responsable = models.ForeignKey(Responsable, null=True,on_delete=models.SET_NULL, verbose_name="Responsable")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_atelier
    
class Chaine(models.Model):
    nom_chaine = models.CharField(max_length=50, null=False, unique=True, verbose_name="Type de machine")
    atelier = models.ForeignKey(Atelier, null=True,on_delete=models.SET_NULL, verbose_name="Chaine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_chaine
    
########################################################################################################################
        
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
    
###################################################################################################################
    
class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=50, null=False, verbose_name="Nom fournisseur")
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Téléphone")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_fournisseur

    
class PieceDetachee(models.Model):
    nom_piecedetache = models.CharField(max_length=100, null=False, verbose_name="Nom de la pièce détachée")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    modele = models.ForeignKey(Modele, on_delete=models.SET_NULL,null=True,verbose_name="Modele")
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
    
#################################################################################################################################
        
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
    image = models.ImageField(upload_to='machines/',null=True, verbose_name="Image")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    pieces_detachees = models.ManyToManyField(PieceDetachee, blank=True, verbose_name="Pièces détachées")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_machine
    
    
# class Status(models.Model):
#     nom_status = models.CharField(max_length=50, null=False, unique=True, verbose_name="Statut")
#     date_creation = models.DateTimeField(auto_now_add=True, null=True)
#     deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
#     def __str__(self):
#         return self.nom_status




