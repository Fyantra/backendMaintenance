from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utilisateur.models import Utilisateur

# Create your models here.
class Endroit(models.Model):        #ex: RDC, R+1, R+2, ....
    nom_endroit = models.CharField(max_length=50, null=False, verbose_name="Endroit")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_endroit
    
class Responsable(models.Model):
    nom_responsable = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Téléphone")
    photo = models.ImageField(upload_to='responsables', null=True, blank=True, verbose_name="Photo")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_responsable
    
class Atelier(models.Model):
    nom_atelier = models.CharField(max_length=50, null=False, verbose_name="Nom d`atelier")
    endroit = models.ForeignKey(Endroit, null=True,on_delete=models.SET_NULL, verbose_name="Endroit")
    responsable = models.ForeignKey(Responsable, null=True,on_delete=models.SET_NULL, verbose_name="Responsable")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_atelier
    
class Chaine(models.Model):
    nom_chaine = models.CharField(max_length=50, null=False, verbose_name="Type de machine")
    atelier = models.ForeignKey(Atelier, null=True,on_delete=models.SET_NULL, verbose_name="Chaine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_chaine
    
########################################################################################################################
        
class Modele(models.Model):
    nom_modele = models.CharField(max_length=50, null=False, verbose_name="Nom du modèle")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_modele
    
    
class Type(models.Model):
    nom_type = models.CharField(max_length=50, null=False, verbose_name="Type de machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_type
    
class NomMachine(models.Model):     ##n`est pas utilisee
    nom_machine = models.CharField(max_length=50, null=False, unique=True, verbose_name="Nom de la machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_machine
    

class Marque(models.Model):
    nom_marque = models.CharField(max_length=50, null=False, verbose_name="Marque de la machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_marque
    
class Status(models.Model):     #status machine
    nom_status = models.CharField(max_length=50, null=False, verbose_name="Nom de status")
    couleur = models.CharField(max_length=10, null=True, blank=True, verbose_name="Code couleur statut")
    identifiant = models.IntegerField(null=False, unique=True ,verbose_name="Identifiant statut machine")
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
    quantite = models.PositiveIntegerField(null=False, default=1 ,verbose_name="Quantite")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Prix unitaire")
    emplacement = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Emplacement")      #emplacement du piece detache
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL,null=True,verbose_name="Fournisseur")
    reference_fabricant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Reference fabricant")
    image = models.ImageField(upload_to='piece_detaches',null=True, blank=True, verbose_name="Image")
    stock_min = models.PositiveIntegerField(null=False, verbose_name="Stock minimum")
    stock_max = models.PositiveIntegerField(null=True, verbose_name="Stock maximum")
    lot_de_reapprovisionnement = models.PositiveSmallIntegerField(null=True, verbose_name="Lot de réapprovisionnement")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_piecedetache
    
class ReapprovisionnementPieceDetachee(models.Model):
    pieces_detachees = models.ForeignKey(PieceDetachee, on_delete=models.CASCADE,verbose_name="Pièce détachée a réapprovisionner")
    prix_piece_detachees = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, verbose_name="Prix unitaire de pièce")
    quantite = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(99999)], verbose_name="Quantité de la pièce détachée")
    date_realisation = models.DateTimeField(null=False, verbose_name="Date de realisation de reapprovisionnement")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return f"Réapprovisionnement de {self.pieces_detachees.nom_piecedetache}"
    
#################################################################################################################################
        
class Machine(models.Model):
    nom_machine = models.CharField(max_length=50, null=False, verbose_name="Nom de machine")
    numero_machine = models.CharField(max_length=100, null=False, default=0, verbose_name="Numero de la machine")
    numero_de_serie = models.CharField(max_length=100, null=False, unique=True, verbose_name="Numero de serie")
    numero_de_moteur = models.CharField(max_length=50, null=True, unique=True, blank=True, verbose_name="Numero de moteur")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL,null=True,verbose_name="Type")     #ex: DDL 9000 C 
    marque = models.ForeignKey(Marque, on_delete=models.SET_NULL,null=True,verbose_name="Marque")
    atelier = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Atelier")
    chaine = models.ForeignKey(Chaine,on_delete=models.SET_NULL,null=True,verbose_name="Chaine")  
    date_mis_en_place = models.DateField(null=True, verbose_name="Date de mise en place")   #debut utilisation
    date_acquisition = models.DateField(null=True, blank=True, verbose_name="Date d'acquisition")   #date d`achat
    identifiant_status_machine = models.IntegerField(null=False, blank=True, default=1 ,verbose_name="Identifiant statut machine")
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
    
class HistoriqueMouvementMachine(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL,null=True,verbose_name="Machine")
    atelier = models.ForeignKey(Atelier,on_delete=models.SET_NULL,null=True,verbose_name="Atelier")
    chaine = models.ForeignKey(Chaine,on_delete=models.SET_NULL,null=True,verbose_name="Chaine")  
    date_deplacement = models.DateTimeField(auto_now=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")

################################################################################################################
class MotifTache(models.Model):     #ex: preventif, priorite basse
    nom_motif_tache = models.CharField(max_length=50, null=False, verbose_name="Nom de motif de tache")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_motif_tache
    
class StatusTache(models.Model):        #ex: termine, annule
    nom_status_tache = models.CharField(max_length=50, null=False, verbose_name="Nom de status de tache")
    couleur = models.CharField(max_length=10, null=True, blank=True, verbose_name="Code couleur statut tache")
    identifiant = models.IntegerField(null=False, unique=True ,verbose_name="Identifiant statut tache")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_status_tache
        
class Tache(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL,null=True,verbose_name="Tache Machine")
    description = models.TextField(null=False,verbose_name="Description tache")
    motif_tache = models.ForeignKey(MotifTache, on_delete=models.SET_NULL,null=True,verbose_name="Motif tache machine")
    identifiant_status_tache = models.IntegerField(null=False, blank=True, default=1 ,verbose_name="Identifiant statut tache")
    date_debut = models.DateField(null=False, verbose_name="Date debut de tache")
    heure_debut = models.TimeField(null=True, blank=True, verbose_name="Heure debut de tache")
    date_fin = models.DateField(null=False, verbose_name="Date fin de tache")
    heure_fin = models.TimeField(null=True, blank=True, verbose_name="Heure fin de tache")
    temps_maintenance_heure = models.PositiveIntegerField(null=True,blank=True, validators=[MaxValueValidator(99999)] , verbose_name="Temps de maintenance en heure")
    temps_maintenance_minute = models.PositiveIntegerField(null=True,default=0, blank=True, validators=[MaxValueValidator(59)] , verbose_name="Temps de maintenance en minute")
    temps_arret_heure = models.PositiveIntegerField(null=True,blank=True, validators=[MaxValueValidator(99999)], verbose_name="Temps d`arret en heure")
    temps_arret_minute = models.PositiveIntegerField(null=True,default=0, blank=True, validators=[MaxValueValidator(59)] , verbose_name="Temps d`arret en minute")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.description
    
class ActiviteTache(models.Model):
    description = models.TextField(max_length=2000, null=False , verbose_name="Description activite tache")
    date_realisation = models.DateTimeField(null=False, verbose_name="Date de realisation d`activite")
    temps_passe_heure = models.PositiveIntegerField(null=True,blank=True, validators=[MaxValueValidator(99999)] , verbose_name="Temps passé sur l`activite en heure")
    temps_passe_minute = models.PositiveIntegerField(null=True,blank=True, validators=[MaxValueValidator(59)] , verbose_name="Temps passé sur l`activite en minute")
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE,verbose_name="Tache associe a l`activite")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.description
    
class ActiviteTachePieceDetachee(models.Model):
    activite_tache = models.ForeignKey(ActiviteTache, related_name='activite_tache', on_delete=models.CASCADE,null=True, verbose_name="Activite")
    pieces_detachees = models.ForeignKey(PieceDetachee, related_name='pieces_detachees', on_delete=models.CASCADE, null=True, verbose_name="Pièce détachée liée a l`activite")
    quantite = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)], verbose_name="Quantité de la pièce détachée liée")
    prix_piece_detachees = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, verbose_name="Prix unitaire de pièce")
    
    # def save(self, *args, **kwargs):
    #     if self.pieces_detachees and self.quantite > self.pieces_detachees.quantite:
    #         raise ValueError("La quantité demandée dépasse la quantité disponible.")
    #     super().save(*args, **kwargs)

    
class HistoriqueTache(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.SET_NULL,null=True,verbose_name="Tache Machine")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
        
class HistoriqueMouvementPieceDetachee(models.Model):
    SOURCE_CHOICES = [
        ('REAPPROVISIONNEMENT', 'Réapprovisionnement'),
        ('CONSOMMATION', 'Consommation'),
        ('RETOUR_CONSOMMATION', 'Retour de consommation'),
        ('INVENTAIRE', 'Inventaire de pièce détachée')
    ]
    
    piece_detachee = models.ForeignKey(PieceDetachee, on_delete=models.CASCADE, verbose_name="Pièce détachée")
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE, null=True, verbose_name="Reference tache")      #pour savoir dans quel tache a eu l`action`
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name="Source du mouvement")
    date_realisation = models.DateTimeField(verbose_name="Date de réalisation")
    quantite = models.IntegerField(verbose_name="Quantité du mouvement")  # Positif pour réapprovisionnement, négatif pour consommation
    cout = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coût du mouvement")
    quantite_piece = models.PositiveIntegerField(verbose_name="Quantité actuelle de la pièce détachée")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.piece_detachee.nom_piecedetache} - {self.source} ({self.date_realisation})"


##################################NOTIFICATION################################
class Notification(models.Model):
    message = models.TextField(verbose_name="Message de la notification")
    piece_detachee = models.ForeignKey(PieceDetachee, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Pièce détachée associée")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    utilisateurs = models.ManyToManyField(
        Utilisateur, through='UserNotification', related_name='notifications', 
        verbose_name="Utilisateurs associés"
    )

    def __str__(self):
        return f"Notification: {self.message}"    

class UserNotification(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    vue = models.BooleanField(default=False, verbose_name="Notification vue")

    def __str__(self):
        return f"User: {self.user.username}, Notification: {self.notification.id}, Vue: {self.vue}"
