from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    climate = models.CharField(max_length=100, blank=True, default='')
    terrain = models.CharField(max_length=100, blank=True, default='')
    appearance_qnt = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
