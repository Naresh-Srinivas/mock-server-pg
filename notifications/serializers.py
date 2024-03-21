from rest_framework import serializers

from .models import *


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """

    class Meta:
        model = Notification
        fields = '__all__'
