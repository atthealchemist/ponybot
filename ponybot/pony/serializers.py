from rest_framework.serializers import ModelSerializer

from .models import Pony


class PonySerializer(ModelSerializer):
    class Meta:
        model = Pony
        fields = '__all__'
