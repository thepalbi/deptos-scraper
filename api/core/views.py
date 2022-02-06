from django.shortcuts import render
from .serializers import PropertySerializer
from .models import Property
from rest_framework import viewsets

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer