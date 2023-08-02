from django.db import models
from core.core import CoreDb


LEVELS_LIST_DISPLAY = ['name']
class Levels(CoreDb):
    name = models.CharField(max_length=350)
    # description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'
    def __str__(self) -> str:
        return f"{self.name}"