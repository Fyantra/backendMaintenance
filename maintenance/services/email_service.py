from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_maintenance_email(subject, to_emails, context, template_name='emails/maintenance_notification.html'):
    """
    Envoie un email concernant une maintenance
    Args:
        subject: Sujet de l'email
        to_emails: Liste des adresses email des destinataires
        context: Dictionnaire de contexte pour le template
        template_name: Chemin vers le template HTML
    """
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)  # Version texte pour les clients email simples
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails,
            reply_to=[settings.DEFAULT_FROM_EMAIL]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False