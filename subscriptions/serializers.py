from rest_framework import serializers

from .models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Subscription model
    """
    class Meta:
        model = Subscription
        fields = '__all__'


class AuthSerializer(serializers.Serializer):
    """
    Serializer for AuthInit Model
    """
    class Meta:
        model = AuthInit
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction Model
    """
    class Meta:
        model = Transaction
        fields = '__all__'
