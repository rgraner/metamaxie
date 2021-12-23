from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from PIL import Image
import uuid
import os


class User(AbstractUser):

    def user_directory_path(instance, filename):
        profile_avatar_name = '{}_{}_{}/{}'.format(instance.type, instance.username, instance.id, filename)
        full_path = os.path.join(settings.MEDIA_ROOT, profile_avatar_name)

        if os.path.exists(full_path):
            os.remove(full_path)

        return profile_avatar_name
    
    class Type(models.TextChoices):
        MANAGER = 'MANAGER', 'Manager'
        SCHOLAR = 'SCHOLAR', 'Scholar'

    type = models.CharField(_('Type'), max_length=50, choices=Type.choices) # default=Type.MANAGER)
    avatar = models.ImageField(upload_to=user_directory_path, default='avatar.png')

    # make uploaded avatar squared
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.height > img.width:
                # make square by cutting off equal amounts top and bottom
                left = 0
                right = img.width
                top = (img.height - img.width)/2
                bottom = (img.height + img.width)/2
                img = img.crop((left, top, right, bottom))
                # Resize the image to 300x300 resolution
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
         
            elif img.width > img.height:
                # make square by cutting off equal amounts left and right
                left = (img.width - img.height)/2
                right = (img.width + img.height)/2
                top = 0
                bottom = img.height
                img = img.crop((left, top, right, bottom))
                # Resize the image to 300x300 resolution
                if img.height > 300 or img.width >300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)


class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.MANAGER)

class ScholarManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.SCHOLAR)


class ManagerTeam(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    team_code = models.CharField(max_length=255)

    def __str__(self):
        return str(self.team_code)

    def save(self, *args, **kwargs):
        if self.team_code=="":
            self.team_code = str(uuid.uuid4()).replace("-","").upper()[:10]
        return super().save(*args, **kwargs)

class Manager(User):
    objects = ManagerManager()

    @property
    def teamcode(self):
        return self.managerteamcode

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.MANAGER
        return super().save(*args, **kwargs)


class ScholarTeam(models.Model):
    scholar = models.OneToOneField(User, on_delete=models.CASCADE)
    team_code = models.ForeignKey(ManagerTeam, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.scholar)

class Scholar(User):
    objects = ScholarManager()

    @property
    def teamcode(self):
        return self.scholarteamcode

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.SCHOLAR
        return super().save(*args, **kwargs)
