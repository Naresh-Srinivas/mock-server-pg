import requests
from rest_framework import status
from rest_framework.response import Response

import subscriptions.models
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


def create_new_notification(data):
    """
    Create a new notification object and store it
    :param data:
    :return:
    """
    notification = Notification.objects.create(
        merchant_id=data['merchant_id'],
        merchant_user_id=data['merchant_user_id'],
        subscription_id=data['subscription_id'],
        transaction_id=data['transaction_id'],
        amount=data['amount'],
        auto_debit=data['auto_debit'])
    serializer = NotificationSerializer(data=notification)
    if serializer.is_valid() and subscriptions.models.Subscription.objects.get(id=data['subscription_id']):
        serializer.save()
    notification = Notification.objects.get(transaction_id=data['transaction_id'])
    if notification:
        notification.state = "ACCEPTED"
        notification.save()


def create_notif_response(notification):
    """
    create a response for notification creation
    :param notification:
    :return:
    """
    response = Response()
    response.success = True
    response.status_code = status.HTTP_200_OK
    response.data = {
        "success": True,
        "code": "SUCCESS",
        "message": "Your request has been successfully submitted.",
        "data": {
            "notificationId": notification.id,
            "state": notification.state,
            "amount": notification.amount
        }
    }
    return response


def create_notif_status_check_response(notification):
    """
    create a response for notification status check
    :param notification:
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
            "notificationId": notification.id,
            "subscriptionId": notification.subscription_id,
            "state": notification.state,
        }
    }
    return response


def send_notification_callback(notification_id):
    """
    Creates and sends a callback notification
    :param notification_id:
    :return:
    """
    notification = Notification.objects.get(id=notification_id)
    if notification.state == "ACCEPTED":
        notification.state = "NOTIFIED"
        notification.save()
        headers = {'Content-Type': 'application/json'}
        url = " "
        payload = {
            "callback_type": "NOTIFY",
            "merchant_id": notification.merchant_id,
            "transaction_id": notification.transaction_id,
            "notification_details": notification,
            "subscription_details": subscriptions.models.Subscription.objects.get(id=notification.subscription_id)
        }
        response = requests.post(url, data=payload, headers=headers)
        return response
