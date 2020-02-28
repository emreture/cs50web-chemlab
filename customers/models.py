from django.db import models
from django.conf import settings
# Create your models here.


class Customer(models.Model):
    """Laboratory customers are legal entities not individuals.
    Field 'name' represents the organization name.
    """
    name = models.CharField(max_length=64)
    address = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="organization")

    def __str__(self):
        return f"{self.name}"
