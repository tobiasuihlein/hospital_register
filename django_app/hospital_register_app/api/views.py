from rest_framework import viewsets, mixins
from .models import HospitalLocations, HospitalDetails
from .serializers import HospitalLocationsSerializer, HospitalDetailsSerializer


class CustomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass

class HospitalLocationsView(CustomViewSet):
    queryset = HospitalLocations.objects.all()
    serializer_class = HospitalLocationsSerializer

class HospitalDetailsView(CustomViewSet):
    queryset = HospitalDetails.objects.all()
    serializer_class = HospitalDetailsSerializer