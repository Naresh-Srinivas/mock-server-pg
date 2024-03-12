from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionSerializer

class CreateSubscriptionView(APIView):
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
        if serializer.is_valid() and check_unique(subscription.merchant_subscription_id):
            serializer.save()
        subscription = Subscription.objects.get(
            merchant_subscription_id=data['merchantSubscriptionId'])
        if subscription:
            subscription.status = "SUCCESS"
        response = Response()
        response.success = True
        response.status_code = status.HTTP_200_OK
        response.data = {
            "success": True,
            "code": "SUCCESS",
            "message": "Your request has been successfully completed",
            "data": {
                "subscriptionId": subscription.id,
                "state": "CREATED",
                "validUpto": 15 * 60 * 60
            }
        }
        return response


def check_unique(subscription_id):
    return Subscription.objects.filter(merchant_subscription_id=subscription_id) is None
