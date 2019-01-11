from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=100, blank=False)
    climate = models.CharField(max_length=100, blank=True, default='')
    terrain = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('name',)
