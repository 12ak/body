from django.db import models

# Create your models here.
from django.conf import settings
from django.urls import reverse
from model_utils.models import TimeStampedModel

class Measurement(TimeStampedModel):
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chest       = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    abdomen     = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh       = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight      = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('tracker:detail', kwargs={'pk': self.pk})

    def get_total_measurement(self):
        return self.chest + self.abdomen + self.thigh
