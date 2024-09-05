# serializers.py
from rest_framework import serializers
from .models import MelbourneSuburbs, Waste, Centre

class MelbourneSuburbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MelbourneSuburbs
        fields = ['postcode', 'suburb']

class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = ['waste_id', 'waste_type']

class CentreSerializer(serializers.ModelSerializer):
    waste = WasteSerializer()  # Include waste details in the response

    class Meta:
        model = Centre
        fields = ['centre_id', 'name', 'address', 'latitude', 'longitude', 'waste']
