from rest_framework import status
from rest_framework.response import Response

import notifications.models
import subscriptions.models
import subscriptions
from .serializers import *
import requests


def create_new_renewal_execute(data):
    """
    Create a new renewal and store it in the database
    :param data:
    :return:
    """
    renewals_execute = Renewal.objects.create(
        merchant_id=data['merchant_id'],
        merchant_user_id=data['merchant_user_id'],
        transaction_id=data['transaction_id'],
        subscription_id=data['subscription_id'],
        notification_id=data['notification_id'])
    serializers = RenewalsExecuteSerializer(data=renewals_execute)
    if serializers.is_valid():
        serializers.save()
    renewal = Renewal.objects.get(transaction_id=data['transaction_id'])
    if renewal:
        renewal.state = "SUCCESS"
        renewal.save()


def create_renewal_debit_response(renewals):
    """
    Create and return response for debit renewals
    :param renewals:
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
            "merchantId": renewals.merchant_id,
            "transactionId": renewals.transaction_id,
            "state": renewals.state,
        }
    }
    return response


def create_renewal_status_check_response(renewals):
    """
    Create and return response for debit renewals
    :param renewals:
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
            "renewalId": renewals.id,
            "transactionId": renewals.transaction_id,
            "state": renewals.state
        }
    }
    return response


def send_renewals_callback(transaction_id):
    """
    Send renewals callback
    :param transaction_id:
    :return:
    """
    renewals = Renewal.objects.get(transaction_id=transaction_id)
    if renewals.state == "SUCCESS":
        headers = {'Content-Type': 'application/json'}
        url = " "
        payload = {
            "callback_type": "DEBIT",
            "merchant_id": renewals.merchant_id,
            "transaction_id": renewals.transaction_id,
            "notification_details": notifications.models.Notification.objects.get(transaction_id=transaction_id),
            "subscription_details": subscriptions.models.Subscription.objects.get(id=renewals.subscription_id)
        }
        response = requests.post(url, data=payload, headers=headers)
        return response
