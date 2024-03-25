from rest_framework.views import APIView
from .utils import *


class CreateSubscriptionView(APIView):
    """
    View for creating subscriptions
    """
    def post(self, request):
        """
        POST method for creating subscriptions and storing in db
        :param request:
        :return:
        """
        data = request.data
        create_new_subscription(data)
        return create_subscription_response(
            Subscription.objects.get(merchant_subscription_id=data['merchantSubscriptionId']))


class FetchSubscriptionView(APIView):
    """
    View for fetching subscriptions
    """
    def get(self, request):
        """
        GET method for fetching the subscriptions from db
        :param request:
        :return:
        """
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusCheckView(APIView):
    """
    View for checking the subscription status
    """
    def get(self, request):
        """
        GET method for checking the subscription status
        :param request:
        :return:
        """
        merchant_id = request.GET.get('merchant_id')
        merchant_subs_id = request.GET.get('merchant_subs_id')
        subscriptions = Subscription.objects.get(
            merchant_id=merchant_id, merchant_subscription_id=merchant_subs_id)
        if subscriptions is None:
            return None
        return create_subs_status_check_response(subscriptions)


class AuthView(APIView):
    """
    View for initiating auth for first transaction
    """
    def post(self, request):
        """
        POST method for creating init auth and storing it in db
        :param request:
        :return:
        """
        data = request.data
        create_new_init_auth(data)
        return create_init_auth_response(data['authRequestId'])


class AuthStatusView(APIView):
    """
    View for checking the init auth status
    """
    def get(self, request):
        """
        GET method for checking the status of init auth
        :param request:
        :return:
        """
        merchant_id = request.GET.get('merchant_id')
        auth_req_id = request.GET.get('auth_req_id')
        auth_init = AuthInit.objects.get(
            merchant_id=merchant_id, auth_req_id=auth_req_id)
        if auth_init is None:
            return None
        return create_auth_status_response(auth_init)


class TransactionView(APIView):
    """
    View for creating first transaction of the subscription
    """
    def post(self, request):
        """
        POST method for creating first transaction and storing it in db
        :param request:
        :return:
        """
        data = request.data
        create_new_transaction(data)
        trans = Transaction.objects.get(subscription_id=data['subscriptionId'])
        if (trans.pay_response_code == "SUCCESS" and
                AuthInit.objects.get(subscription_id=data['subscriptionId']).state == "CREATED"):
            mark_subs_active(data['subscriptionId'])
            send_subs_success_callback(trans.subscription_id)
        else:
            mark_subs_failed(data['subscriptionId'])
        return create_transaction_response(data['subscriptionId'])


class CancelSubscriptionView(APIView):
    """
    View for cancelling a subscription
    """
    def post(self, request):
        """
        POST method for cancelling a subscription
        :param request:
        :return:
        """
        data = request.data
        initiate_subs_cancellation(data)
        return initiate_subs_cancel_response(data)


class CancelCallbackView(APIView):
    """
    View for sending subscription cancellation callback
    """
    def post(self, request):
        """
        POST method for sending subscription cancellation callback
        :param request:
        :return:
        """
        data = request.data
        subs = Subscription.objects.get(id=data['subscriptionId'])
        if subs.state == "CANCEL_IN_PROGRESS":
            mark_subs_cancelled_and_send_callback(data['subscriptionId'])
        return Response(status= status.HTTP_200_OK)


