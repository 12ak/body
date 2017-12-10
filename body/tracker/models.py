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

    #TODO make these fields reference to the User class
    height      = 179.0
    gender      = "male"
    age         = 28.0
    # birthday    =
    # age         = User.get_age() > should this be a pointer?

    def get_absolute_url(self):
        return reverse('tracker:detail', kwargs={'pk': self.pk})

    def get_calculations(self):
        total_measurement   = float(self.chest + self.abdomen + self.thigh)
        age                 = float(self.age)
        weight              = float(self.weight)
        height              = float(self.height)

        bone_density = (
                + 1.1093800
                - (0.0008267 * total_measurement)
                + (0.0000016 * total_measurement * total_measurement)
                - (0.0002574 * age)
            );
        body_fat_percentage = ((4.95 / bone_density) - 4.5) * 100
        fat_kg = weight * body_fat_percentage / 100
        muscle_kg = weight - fat_kg

        calculations = {
                'body_fat_percentage': body_fat_percentage,
                'muscle_kg': muscle_kg,
                'fat_kg': fat_kg,
                'total_measurement': total_measurement
            }

        return calculations
