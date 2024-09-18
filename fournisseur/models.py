from django.db import models

# Create your models here.

class Fournisseur(models.Model):
    nom_fournisseur = models.CharField(max_length=50, null=False, verbose_name="Nom fournisseur")
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Téléphone")
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateField(null=True, blank=True, verbose_name="Date de suppression")
    
    def __str__(self):
        return self.nom_fournisseur