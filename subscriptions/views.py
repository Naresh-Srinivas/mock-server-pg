from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionSerializer
from .utils import *


class CreateSubscriptionView(APIView):
    def post(self, request):
        data = request.data
        create_subscription(data)
        return create_subscription_response(
            Subscription.objects.get(merchant_subscription_id=data['merchantSubscriptionId'])
        )

class FetchSubscriptionView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


