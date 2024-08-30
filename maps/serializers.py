from rest_framework import serializers
# from .models import Waste
# from rest_framework import serializers
from .models import Waste, Centre  # Ensure both Waste and Centre are imported

class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = '__all__'

class CentreSerializer(serializers.ModelSerializer):
    waste = WasteSerializer()  # This will nest the WasteSerializer inside the CentreSerializer

    class Meta:
        model = Centre
        fields = '__all__'