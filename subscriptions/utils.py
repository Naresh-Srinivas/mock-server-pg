from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response

from .models import *
from .serializers import *


def check_if_subs_id_unique(subscription_id):
    return Subscription.objects.filter(merchant_subscription_id=subscription_id) is None


def create_subscription(data):
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
    if (serializer.is_valid()
            and check_if_subs_id_unique(subscription.merchant_subscription_id)):
        serializer.save()
    subscription = Subscription.objects.get(
        merchant_subscription_id=data['merchantSubscriptionId'])
    if subscription:
        subscription.state = "CREATED"
        subscription.save()


def create_subscription_response(subscription):
    response = Response()
    response.success = True
    response.status_code = status.HTTP_200_OK
    response.data = {
        "success": True,
        "code": "SUCCESS",
        "message": "Your request has been successfully completed",
        "data": {
            "subscriptionId": subscription.id,
            "state": subscription.state,
            "validUpto": 15 * 60 * 60
        }
    }
    return response


