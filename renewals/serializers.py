from rest_framework import serializers

from .models import *


class RenewalsExecuteSerializer(serializers.ModelSerializer):
    """
    Serializer for Renewals model
    """
    class Meta:
        model = Renewal
        fields = '__all__'
