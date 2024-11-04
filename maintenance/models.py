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
    
class Status(models.Model):
    nom_status = models.CharField(max_length=50, null=False, verbose_name="Nom de status")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_status
    
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
    date_achat = models.DateTimeField(null=True, blank=True, verbose_name="Date d'achat")
    quantite = models.PositiveIntegerField(null=False, default=0 ,verbose_name="Quantite")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Prix unitaire")
    emplacement = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Emplacement")      #emplacement du piece detache
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    image = models.ImageField(upload_to='piece_detaches',null=True, verbose_name="Image")
    stock_min = models.PositiveIntegerField(null=False, verbose_name="Stock minimum")
    stock_max = models.PositiveIntegerField(null=True, verbose_name="Stock maximum")
    lot_de_reapprovisionnement = models.PositiveSmallIntegerField(null=True, verbose_name="Lot de réapprovisionnement")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_piecedetache
    
#################################################################################################################################
        
class Machine(models.Model):
    nom_machine = models.CharField(max_length=50, null=False, verbose_name="Nom de machine")
    numero_de_serie = models.CharField(max_length=100, null=False, unique=True, verbose_name="Numero de serie")
    numero_de_moteur = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numero de moteur")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL,null=True,verbose_name="Type")     #ex: DDL 9000 C 
    marque = models.ForeignKey(Marque, on_delete=models.SET_NULL,null=True,verbose_name="Marque")
    atelier = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Atelier")
    chaine = models.ForeignKey(Chaine,on_delete=models.SET_NULL,null=True,verbose_name="Chaine")  
    date_mis_en_place = models.DateField(null=True, verbose_name="Date de mise en place")   #debut utilisation
    date_acquisition = models.DateField(null=True, blank=True, verbose_name="Date d'acquisition")   #date d`achat
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=False,verbose_name="Status")
    date_hors_service= models.DateField(null=True, blank=True, verbose_name="Date de mise hors service") 
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='machines/',null=True, verbose_name="Image machine")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    pieces_detachees = models.ManyToManyField(PieceDetachee, blank=True, verbose_name="Pièces détachées")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_machine
    
class MachineRelation(models.Model):        #pour les machines qui ont des machines associes
    machine_principale = models.ForeignKey(Machine, related_name='machine_principale', on_delete=models.CASCADE,null=True, verbose_name="Machine principale")
    machine_liee = models.ForeignKey(Machine, related_name='machine_liee', on_delete=models.CASCADE, null=True, verbose_name="Machine liée")
    quantite = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantité de la machine liée")
    
    def __str__(self):
        return f"{self.machine_principale.nom_machine} liée à {self.machine_liee.nom_machine} (Quantité: {self.quantite})"
    



