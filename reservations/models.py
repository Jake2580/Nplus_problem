from django.db import models

# Create your models here.
class Reservation(models.Model):
    content = models.TextField()
    owner_id = models.ForeignKey(
        "Owner",
        related_name="owner",
        on_delete=models.CASCADE,
        db_column="owner_id"
    )

class Owner(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=20)
