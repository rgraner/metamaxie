from django.db import models

from .validators import validate_ronin
from users.models import Scholar, Manager


class Ronin(models.Model):
    ronin = models.CharField(unique=True, max_length=46, validators=[validate_ronin])
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.ronin)


class Scholarship(models.Model):
    scholarship = models.CharField(max_length=200, blank=True, null=True)
    scholar = models.ForeignKey(Scholar, on_delete=models.DO_NOTHING ,blank=True, null=True)
    ronin = models.OneToOneField(Ronin, on_delete=models.CASCADE, blank=True, null=True)
    lifetime_slp = models.IntegerField(blank=True, null=True)
    built_up_slp = models.IntegerField(blank=True, null=True)
    last_claim = models.DateTimeField(blank=True, null=True)
    total_slp = models.IntegerField(blank=True, null=True)
    in_game_slp = models.IntegerField(blank=True, null=True)
    mmr = models.BigIntegerField(blank=True, null=True)
    daily_average = models.FloatField(blank=True, null=True)
    daily_slp_earned = models.FloatField(blank=True, null=True)
    daily_slp_paid = models.FloatField(blank=True, null=True)
    daily_fiat_earned = models.FloatField(blank=True, null=True)
    daily_fiat_paid = models.FloatField(blank=True, null=True)
    next_claim = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True, related_name='scholarship_manager')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.scholarship)


class TotalDailySlp(models.Model):
    total_daily_slp_earned = models.FloatField(blank=True, null=True)
    total_daily_slp_paid = models.FloatField(blank=True, null=True)
    total_daily_fiat_earned = models.FloatField(blank=True, null=True)
    total_daily_fiat_paid = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.owner)

        


