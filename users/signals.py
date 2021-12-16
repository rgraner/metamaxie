from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Manager, ScholarTeam, ManagerTeam


# signal for custom authentication
@receiver(post_save, sender=User)
def post_save_create_scholarship_payment(sender, instance, created, **kwargs):
    if created:
        managers = Manager.objects.all()

        if instance in managers:
            ManagerTeam.objects.create(manager=instance)
        else:
            ScholarTeam.objects.create(scholar=instance)