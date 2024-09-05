from django.db import models

class MelbourneSuburbs(models.Model):
    postcode = models.IntegerField(primary_key=True)
    suburb = models.CharField(max_length=50)

    class Meta:
        db_table = 'Melbourne_suburbs'
        managed = False

    def __str__(self):
        return f"{self.suburb} (Postcode: {self.postcode})"
        # This returns a string like "Melbourne (Postcode: 3000)" when you print a MelbourneSuburbs object

class Waste(models.Model):
    waste_id = models.IntegerField(primary_key=True)
    waste_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'Waste'
        managed = False

    def __str__(self):
        return self.waste_type
        # This returns the type of waste, e.g., "Organic" or "Recyclable"

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

    def __str__(self):
        return f"{self.name} - {self.address}"