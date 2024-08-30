from rest_framework import viewsets
from .models import Waste
from .serializers import WasteSerializer
from .models import Centre
from .serializers import CentreSerializer

class WasteViewSet(viewsets.ModelViewSet):
    queryset = Waste.objects.all()
    serializer_class = WasteSerializer


class CentreViewSet(viewsets.ModelViewSet):
    queryset = Centre.objects.all()
    serializer_class = CentreSerializer