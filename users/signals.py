from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User, Manager, ScholarTeam, ManagerTeam

#import os


# signal for custom authentication
@receiver(post_save, sender=User)
def post_save_create_scholarship_payment(sender, instance, created, **kwargs):
    if created:
        managers = Manager.objects.all()

        if instance in managers:
            ManagerTeam.objects.create(manager=instance)
        else:
            ScholarTeam.objects.create(scholar=instance)


# @receiver(post_delete, sender=User)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.avatar:
#         if os.path.isfile(instance.avatar.path):
#             os.remove(instance.avatar.path)