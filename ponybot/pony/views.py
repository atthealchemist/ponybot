from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Pony
from .serializers import PonySerializer

# Create your views here.


class PonyViewSet(ModelViewSet):
    queryset = Pony.objects.all()
    serializer_class = PonySerializer
