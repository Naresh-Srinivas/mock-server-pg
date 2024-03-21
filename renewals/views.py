from django.shortcuts import render
from rest_framework.views import APIView
from .utils import *
from .models import *


# Create your views here.
class RenewalsExecuteView(APIView):
    """
    View to execute renewal debit
    """

    def post(self, request):
        data = request.data
        create_new_renewal_execute(data)
        return create_renewal_debit_response(
            Renewal.objects.get(transaction_id=data['transaction_id']))


class RenewalsStatusCheckView(APIView):
    """
    View to status check for renewals
    """

    def get(self, request):
        transaction_id = request.GET.get('transaction_id')
        renewal = Renewal.objects.get(transaction_id=transaction_id)
        if renewal is None:
            return None
        return create_renewal_status_check_response(renewal)


class RenewalsCallbackView(APIView):
    """
    View to renewals callback
    """

    def post(self, request):
        """
        POST method for sending renewals debit callback
        :param request:
        :return:
        """
        data = request.data
        renewals = Renewal.objects.get(transaction_id=data['transaction_id'])
        if renewals.state == "SUCCESS":
            send_renewals_callback(data['transaction_id'])
        return Response(status=status.HTTP_200_OK)