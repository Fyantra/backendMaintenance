from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=50, choices=[
        ('chef', 'Administrateur'),
        ('technicien', 'Technicien'),
        ('responsable', 'Responsable')
    ])
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True, null=False)

    # Ajout de related_name pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name='utilisateur_groups',  
        blank=True,
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='utilisateur_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
