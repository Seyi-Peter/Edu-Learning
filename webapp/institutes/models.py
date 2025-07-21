from django.db import models

# Create your models here.
class Institute(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    official_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    