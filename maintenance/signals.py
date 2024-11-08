from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Machine, HistoriqueMouvementMachine

@receiver(pre_save, sender=Machine)
def store_initial_values(sender, instance, **kwargs):
    """Avant de sauvegarder, stocke l'état initial de l'atelier et de la chaîne pour comparaison."""
    if instance.pk:  # S'assure que ce n'est pas une nouvelle instance
        try:
            initial_instance = Machine.objects.get(pk=instance.pk)
            instance._initial_atelier = initial_instance.atelier
            instance._initial_chaine = initial_instance.chaine
        except Machine.DoesNotExist:
            instance._initial_atelier = None
            instance._initial_chaine = None
    else:
        instance._initial_atelier = None
        instance._initial_chaine = None

@receiver(post_save, sender=Machine)
def create_historique_mouvement(sender, instance, created, **kwargs):
    """Crée une entrée dans HistoriqueMouvementMachine à la création ou lors des changements d'atelier/chaîne."""
    if created:
        # Enregistre l'historique pour une nouvelle machine
        HistoriqueMouvementMachine.objects.create(
            machine=instance,
            atelier=instance.atelier,
            chaine=instance.chaine
        )
    else:
        # Vérifie si l'atelier ou la chaîne ont changé
        atelier_changed = instance.atelier != instance._initial_atelier
        chaine_changed = instance.chaine != instance._initial_chaine

        if atelier_changed or chaine_changed:
            # Enregistre l'historique si l'atelier ou la chaîne a changé
            HistoriqueMouvementMachine.objects.create(
                machine=instance,
                atelier=instance.atelier,
                chaine=instance.chaine
            )
