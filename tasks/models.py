from django.db import models
from users.models import ScholarTeam, User 


class Task(models.Model):
    name = models.CharField(max_length=200)
    task_1 = models.IntegerField()
    task_2 = models.IntegerField(blank=True, null=True)
    task_3 = models.IntegerField(blank=True, null=True)
    task_4 = models.IntegerField(blank=True, null=True)
    rate_1 = models.IntegerField()
    rate_2 = models.IntegerField(blank=True, null=True)
    rate_3 = models.IntegerField(blank=True, null=True)
    rate_4 = models.IntegerField(blank=True, null=True)
    rate_5 = models.IntegerField(blank=True, null=True)
    fixed_rate = models.BooleanField(default=False)
    scholar = models.ManyToManyField(ScholarTeam, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
