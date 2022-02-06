from .models import RealEstate
from rest_framework import serializers


class RealEstateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RealEstate
        fields = ["url"]
