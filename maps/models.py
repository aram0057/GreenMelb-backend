

from django.db import models

# from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class MelbourneSuburbs(models.Model):
    postcode = models.IntegerField(primary_key=True)
    suburb = models.CharField(max_length=50)

    class Meta:
        db_table = 'Melbourne_suburbs'
        managed = False

class Waste(models.Model):
    waste_id = models.IntegerField(primary_key=True)
    waste_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'Waste'
        managed = False

class Centre(models.Model):
    centre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    waste = models.ForeignKey(Waste, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Centre'
        managed = False