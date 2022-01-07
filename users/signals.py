from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User, Manager, ScholarTeam, ManagerTeam
from metamaxie_proj.settings import MEDIA_ROOT

import os
import shutil


# signal for custom authentication
@receiver(post_save, sender=User)
def post_save_create_scholarship_payment(sender, instance, created, **kwargs):
    if created:
        managers = Manager.objects.all()

        if instance in managers:
            ManagerTeam.objects.create(manager=instance)
        else:
            ScholarTeam.objects.create(scholar=instance)


@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    profile_avatar_name = '{}_{}_{}'.format(instance.type, instance.username, instance.id)
    path = os.path.join(MEDIA_ROOT, profile_avatar_name)
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.avatar:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False, onerror=None)


# @receiver(post_delete, sender=User)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.avatar:
#         if os.path.isfile(instance.avatar.path):
#             os.remove(instance.avatar.path)