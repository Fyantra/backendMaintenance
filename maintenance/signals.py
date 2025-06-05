from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import *
from django.utils import timezone
from django.db.models import F

@receiver(pre_save, sender=Machine)     #deplacement d`un machine
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
            
@receiver(post_save, sender=Machine)        #supprimer les taches associes a ce machine
def delete_related_taches(sender, instance, **kwargs):
    if instance.deleted_at:
        Tache.objects.filter(machine=instance, deleted_at__isnull=True).update(deleted_at=timezone.now())

@receiver(post_save, sender=Tache)
def create_historique_tache(sender, instance, created, **kwargs):
    if created:
        # Enregistre l'historique pour une nouvelle tache
        HistoriqueTache.objects.create(
            tache=instance,
        )
    else:
        return
            
@receiver(post_delete, sender=ActiviteTachePieceDetachee)     #en cas de suppression d`un activite, la quantite de PD doit revenir a l`initial 
def restore_piece_detachee_quantite(sender, instance, **kwargs):
    piece_detachee = instance.pieces_detachees
    if piece_detachee:
        # Restaurer la quantité
        piece_detachee.quantite += instance.quantite
        piece_detachee.save()

        # Calcul du coût
        cout = instance.quantite * instance.prix_piece_detachees

        # Enregistrement dans l'historique des mouvements
        HistoriqueMouvementPieceDetachee.objects.create(
            piece_detachee=piece_detachee,
            tache = instance.activite_tache.tache,
            source='Retour de consommation',
            date_realisation=timezone.now(),
            quantite=instance.quantite,
            cout=cout,
            quantite_piece=piece_detachee.quantite  # Quantité actuelle après le retour
        )


@receiver(post_save, sender=PieceDetachee)
def verifier_stock_limites(sender, instance, **kwargs):
    utilisateurs = Utilisateur.objects.all()
    notifications = []
    user_notifications = []

    # Vérification du stock minimum
    if instance.quantite < instance.stock_min:
        notification_min = Notification.objects.create(
            piece_detachee=instance,
            message="Le stock de la pièce détachée '{}' est passé sous le seuil minimal.".format(instance.nom_piecedetache),
        )
        notifications.append(notification_min)

    # Vérification du stock maximum
    if instance.stock_max and instance.quantite > instance.stock_max:
        notification_max = Notification.objects.create(
            piece_detachee=instance,
            message="Le stock de la pièce détachée '{}' a dépassé le seuil maximal.".format(instance.nom_piecedetache),
        )
        notifications.append(notification_max)

    # Associer les notifications à tous les utilisateurs
    for notification in notifications:
        user_notifications.extend(
            [UserNotification(user=user, notification=notification) for user in utilisateurs]
        )

    if user_notifications:
        UserNotification.objects.bulk_create(user_notifications)

#notification pour les changements de statut des tâches
@receiver(post_save, sender=Tache)
def verifier_statut_tache(sender, instance, created, **kwargs):
    # Ne pas créer de notification pour les nouvelles tâches
    if created:
        return

    utilisateurs = Utilisateur.objects.all()
    notifications = []
    user_notifications = []

    # Vérification des changements de statut
    if instance.identifiant_status_tache == 4:
        notification = Notification.objects.create(
            tache=instance,
            message=f"La tâche '{instance.nom_tache}' a été marquée comme terminée.",
        )
        notifications.append(notification)
    elif instance.identifiant_status_tache == 3:
        notification = Notification.objects.create(
            tache=instance,
            message=f"La tâche '{instance.nom_tache}' est en retard!",
        )
        notifications.append(notification)

    # Associer les notifications à tous les utilisateurs
    for notification in notifications:
        user_notifications.extend(
            [UserNotification(user=user, notification=notification) for user in utilisateurs]
        )

    if user_notifications:
        UserNotification.objects.bulk_create(user_notifications)
        
STATUS_MACHINE = {
    1: "La machine a été mise en service",
    2: "La machine a été mise en maintenance", 
    3: "La machine a été mise hors-service",
    4: "La machine est en panne"
}

STATUS_TACHE = {
    1: "La tâche est planifiée",
    2: "La tâche est en cours",
    4: "La tâche est terminée",
    5: "La tâche est annulée",
    6: "La tâche est en retard et commencée"
}

@receiver(pre_save, sender=Machine)
def store_initial_machine_status(sender, instance, **kwargs):
    """Stocke le statut initial avant sauvegarde"""
    if instance.pk:
        try:
            old_instance = Machine.objects.get(pk=instance.pk)
            instance._initial_status = old_instance.identifiant_status_machine
        except Machine.DoesNotExist:
            instance._initial_status = None
    else:
        instance._initial_status = None

@receiver(post_save, sender=Machine)
def create_machine_status_history(sender, instance, created, **kwargs):
    """Crée l'historique des statuts de machine"""
    current_status = instance.identifiant_status_machine
    
    if current_status not in STATUS_MACHINE:
        return
    
    if created:
        # Création initiale
        HistoriqueStatutMachine.objects.create(
            machine=instance,
            description=STATUS_MACHINE[current_status]
        )
    else:
        # Vérifie si le statut a changé
        if hasattr(instance, '_initial_status') and instance._initial_status != current_status:
            HistoriqueStatutMachine.objects.create(
                machine=instance,
                description=STATUS_MACHINE[current_status]
            )

@receiver(pre_save, sender=Tache)
def store_initial_tache_status(sender, instance, **kwargs):
    """Stocke le statut initial avant sauvegarde"""
    if instance.pk:
        try:
            old_instance = Tache.objects.get(pk=instance.pk)
            instance._initial_status = old_instance.identifiant_status_tache
        except Tache.DoesNotExist:
            instance._initial_status = None
    else:
        instance._initial_status = None

@receiver(post_save, sender=Tache)
def create_tache_status_history(sender, instance, created, **kwargs):
    """Crée l'historique des statuts de tâche"""
    current_status = instance.identifiant_status_tache
    
    if current_status not in STATUS_TACHE:
        return
    
    if created:
        # Création initiale
        HistoriqueStatutTache.objects.create(
            tache=instance,
            description=STATUS_TACHE[current_status]
        )
    else:
        # Vérifie si le statut a changé
        if hasattr(instance, '_initial_status') and instance._initial_status != current_status:
            HistoriqueStatutTache.objects.create(
                tache=instance,
                description=f"Changement de statut: {STATUS_TACHE[current_status]}"
            )