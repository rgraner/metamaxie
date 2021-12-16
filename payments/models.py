from django.db import models
from users.models import Manager, Scholar


class Payment(models.Model):
    scholarship = models.CharField(max_length=200, blank=True, null=True)
    scholar = models.ForeignKey(Scholar, on_delete=models.DO_NOTHING, blank=True, null=True)
    ronin = models.CharField(max_length=200)
    ronin_slp = models.IntegerField(blank=True, null=True)
    lifetime_slp = models.IntegerField(blank=True, null=True)
    built_up_slp = models.IntegerField(blank=True, null=True)
    last_claim = models.DateTimeField(blank=True, null=True)
    average = models.FloatField(blank=True, null=True)
    slp_paid = models.IntegerField(blank=True, null=True)
    slp_earned = models.IntegerField(blank=True, null=True)
    fiat_paid = models.IntegerField(blank=True, null=True)
    fiat_earned = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True, related_name='payment_manager')

    def __str__(self):
        return str(self.scholarship)


class TotalSlp(models.Model):
    total_slp_earned = models.FloatField(blank=True, null=True)
    total_slp_paid = models.FloatField(blank=True, null=True)
    total_fiat_earned = models.FloatField(blank=True, null=True)
    total_fiat_paid = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.owner)


class TotalScholarSlp(models.Model):
    total_slp_earned = models.FloatField(blank=True, null=True)
    total_fiat_earned = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(Scholar, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.owner)
