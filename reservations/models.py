from django.db import models

# Create your models here.
class Reservation(models.Model):
    context = models.TextField()
    owner = models.ForeignKey(
        'Owner',
        related_name="owners",
        related_query_name="owner",
        on_delete=models.CASCADE,
        db_column="owner"
    )

class Owner(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=20)
