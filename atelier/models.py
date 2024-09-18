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
    