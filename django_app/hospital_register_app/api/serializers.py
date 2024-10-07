from rest_framework import serializers
from .models import HospitalLocations
from .models import HospitalDetails

class HospitalLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalLocations
        fields = '__all__'

class HospitalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDetails
        fields = '__all__'