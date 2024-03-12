from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionSerializer

class CreateSubscriptionView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        subscription = Subscription.objects.create(
            merchant_id=data['merchantId'],
            merchant_subscription_id=data['merchantSubscriptionId'],
            merchant_user_id=data['merchantUserId'],
            auth_workflow_type=data['authWorkflowType'],
            amount_type=data['amountType'],
            amount=data['amount'],
            frequency=data['frequency'],
            recurring_count=data['recurringCount'],
            mobile_number=data['mobileNumber'])
        serializer = SubscriptionSerializer(data=subscription)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

