from dataclasses import fields
from rest_framework import serializers

from admission.models import GoDown

# GoDown Serializer
class GoDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoDown
        fields = '__all__'
