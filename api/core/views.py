from django.shortcuts import render
from .serializers import RealEstateSerializer
from .models import RealEstate
from rest_framework import viewsets

class RealEstateViewSet(viewsets.ModelViewSet):
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer