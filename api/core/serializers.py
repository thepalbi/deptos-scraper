from .models import Property
from rest_framework import serializers


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Property
        fields = ["url"]
