from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import UpdateAPIView

from .models import Pony
from .serializers import PonySerializer

# Create your views here.


class PonyViewSet(ModelViewSet):
    queryset = Pony.objects.all()
    serializer_class = PonySerializer

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
