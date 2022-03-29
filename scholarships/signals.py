from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Scholarship, Ronin
from api.external_api import external_api


@receiver(post_save, sender=Ronin)
def post_save_update_scholarship(sender, instance, **kwargs):

    api = external_api(instance.owner)

    for item in api:
        s, _ = Scholarship.objects.filter(owner=instance.owner).get_or_create(scholarship=item['name'])
        s.lifetime_slp = item['lifetime_slp']
        s.last_claim= item['last_claim']
        s.total_slp = item['total_slp']
        s.in_game_slp = item['in_game_slp']
        s.mmr = item['mmr']
        s.owner = instance.owner
        s.save()

    obj = Scholarship.objects.last()
    ronin = Ronin.objects.last()
    obj.ronin = ronin
    obj.save()

