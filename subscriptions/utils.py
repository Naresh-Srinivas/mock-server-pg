from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

from .serializers import *
import requests


def check_if_subs_id_unique(subscription_id):
    """
    Checks if the subscription is already present or not
    :param subscription_id:
    :return:
    """
    return Subscription.objects.filter(merchant_subscription_id=subscription_id) is None


def create_new_subscription(data):
    """
    Creates a new subscription object and stores it in the db
    :param data:
    :return:
    """
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
    """
    Creates a response body for the subscription created
    :param subscription:
    :return:
    """
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
            "validUpto": timezone.now() + timedelta(minutes=15)
        }
    }
    return response


def create_subs_status_check_response(subscription):
    """
    Creates a response body for the subscription status check
    :param subscription:
    :return:
    """
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
            "stateStartDate": subscription.created_at,
            "stateEndDate": subscription.created_at + timedelta(minutes=15),
            "validUpto": timezone.now() + timedelta(minutes=15)
        }
    }
    return response


def create_new_init_auth(auth):
    """
    Creates a new auth init object and stores it in the db
    :param auth:
    :return:
    """
    auth_data = AuthInit.objects.create(
        merchant_id=auth["merchantId"],
        merchant_user_id=auth["merchantUserId"],
        subscription_id=auth["subscriptionId"],
        auth_req_id=auth["authRequestId"],
        amount=auth["amount"],
        subscription_flow_type=auth["subscriptionFlowType"])
    subs = Subscription.objects.get(id=auth["subscriptionId"])
    if subs and subs.state == "CREATED":
        serializer = AuthSerializer(data=auth_data)
        if serializer.is_valid():
            serializer.save()

    auth_init = AuthInit.objects.get(auth_req_id=auth["authRequestId"])

    if auth_init:
        auth_init.state = "CREATED"
        auth_init.save()


def create_init_auth_response(auth_req_id):
    """
    Creates a response body for the auth init created
    :param auth_req_id:
    :return:
    """
    response = Response()
    if AuthInit.objects.filter(auth_req_id=auth_req_id).exists():
        response.success = True
        response.status_code = status.HTTP_200_OK
        response.data = {
            "success": True,
            "code": "SUCCESS",
            "message": "Your request has been successfully completed",
            "data": {
                "redirect_type": "INTENT",
                "redirect_url": "https://phonePe.com"
            }
        }
        return response


def create_auth_status_response(auth):
    """
    Creates a response body for the auth init status check
    :param auth:
    :return:
    """
    subs = Subscription.objects.get(id=auth.subscription_id)
    response = Response()
    response.success = True
    response.status_code = status.HTTP_200_OK
    response.data = {
        "success": True,
        "code": "SUCCESS",
        "message": "Your Subscription is created",
        "data": {
            "merchantId": auth.merchant_id,
            "authRequestId": auth.auth_req_id,
            "subscriptionDetails": {
                "subscriptionId": subs.id,
                "subscriptionState": subs.state
            }

        }
    }
    return response


def create_new_transaction(transaction):
    """
    Creates a new transaction object and stores it in the db
    :param transaction:
    :return:
    """
    trans = Transaction.objects.create(
        merchant_id=transaction["merchantId"],
        subscription_id=transaction["subscriptionId"],
        auth_req_id=transaction["authRequestId"],
        amount=transaction["amount"])
    serializer = TransactionSerializer(data=trans)
    if serializer.is_valid():
        serializer.save()

    trans_data = Transaction.objects.get(subscription_id=transaction["subscriptionId"])
    if trans_data:
        trans_data.state = "COMPLETED"
        trans_data.pay_response_code = "SUCCESS"
        trans_data.save()


def mark_subs_active(subscription_id):
    """
    Marks a subscription as ACTIVE
    :param subscription_id:
    :return:
    """
    subs = Subscription.objects.get(id=subscription_id)
    if subs is None:
        return None
    subs.state = "ACTIVE"
    subs.save()


def create_transaction_response(subscription_id):
    """
    Creates a response body for transaction created
    :param subscription_id:
    :return:
    """
    transaction = Transaction.objects.get(subscription_id=subscription_id)
    subs = Subscription.objects.get(id=subscription_id)
    response = Response()
    response.success = True
    response.status_code = status.HTTP_200_OK
    response.data = {
        "success": True,
        "code": "SUCCESS",
        "message": "Your Subscription is Active",
        "data": {
            "transaction_details": TransactionSerializer(transaction).data,
            "subscription_details": SubscriptionSerializer(subs).data
        }
    }
    return response


def send_subs_success_callback(subscription_id):
    headers = {'Content-Type': 'application/json'}
    url = " "
    payload = {
        "callback_type": "SUBSCRIPTION_STATUS",
        "subscription_id": subscription_id,
        "status": "ACTIVE"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response
