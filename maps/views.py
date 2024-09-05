# maps/views.py

from rest_framework import viewsets
from .models import MelbourneSuburbs, Waste, Centre
from .serializers import MelbourneSuburbsSerializer, WasteSerializer, CentreSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class MelbourneSuburbsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MelbourneSuburbs.objects.all()
    serializer_class = MelbourneSuburbsSerializer

class WasteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Waste.objects.all()
    serializer_class = WasteSerializer

# Option 1: Function-Based View (if not using a ViewSet for Centres)
@api_view(['GET'])
def filter_locations(request):
    waste_type = request.GET.get('waste_type', None)
    postcode = request.GET.get('postcode', None)

    centres = Centre.objects.all()

    if waste_type:
        centres = centres.filter(waste__waste_type=waste_type)

    if postcode:
        centres = centres.filter(address__icontains=postcode)

    serializer = CentreSerializer(centres, many=True)
    return Response(serializer.data)

# Option 2: Class-Based View (if using a ViewSet for Centres)
class CentreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Centre.objects.all()
    serializer_class = CentreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        waste_type = self.request.query_params.get('waste_type', None)
        postcode = self.request.query_params.get('postcode', None)

        if waste_type:
            queryset = queryset.filter(waste__waste_type=waste_type)
        
        if postcode:
            queryset = queryset.filter(address__icontains=postcode)

        return queryset
