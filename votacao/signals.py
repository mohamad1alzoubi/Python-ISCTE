from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Questao

@receiver(post_save, sender=Questao)
def send_question_notification(sender, instance, created, **kwargs):
    if created:  # Only send notification for new questions
        # Get all users (in a real app, you might want to filter by preferences)
        users = User.objects.filter(is_active=True)
        
        subject = f'Nova Questão: {instance.questao_texto[:50]}...'
        message = f"""
        Uma nova questão foi criada no Sistema de Votação!
        
        Questão: {instance.questao_texto}
        Data de Publicação: {instance.pub_data.strftime('%d/%m/%Y %H:%M')}
        
        Acesse: {settings.SITE_URL}/votacao/{instance.id}/
        
        Vote agora e participe da decisão!
        """
        
        # Send email to all users
        for user in users:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,  # Don't fail if email sending fails
                )
            except Exception as e:
                # Log the error but don't break the application
                print(f"Failed to send email to {user.email}: {e}")

@receiver(post_save, sender=Questao)
def log_question_creation(sender, instance, created, **kwargs):
    if created:
        print(f"Nova questão criada: {instance.questao_texto} (ID: {instance.id})")
