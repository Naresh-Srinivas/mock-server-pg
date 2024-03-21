from django.shortcuts import render
from rest_framework.views import APIView
from .models import *

from .utils import *


# Create your views here.
class CreateNotificationView(APIView):
    """
    View to create a new notification and store it in the database
    """

    def post(self, request):
        """
        Post request to create a new notification
        :param request:
        :return:
        """
        data = request.data
        create_new_notification(data)
        return create_notif_response(Notification.objects.get(transaction_id=data['transaction_id']))


class StatusNotificationView(APIView):
    def get(self, request):
        """
        GET method for checking the subscription status
        :param request:
        :return:
        """
        notification_id = request.GET.get('notification_id')
        notifications = Notification.objects.get(id=notification_id)
        if notifications is None:
            return None
        return create_notif_status_check_response(notifications)


class CallbackNotificationView(APIView):
    """
    View to send a notification callback
    """
    def post(self, request):
        """
        POST method for sending notification callback
        :param request:
        :return:
        """
        data = request.data
        notification = Notification.objects.get(id=data['notification_id'])
        if notification.state == "ACCEPTED":
            send_notification_callback(data['notification_id'])
        return Response(status= status.HTTP_200_OK)
