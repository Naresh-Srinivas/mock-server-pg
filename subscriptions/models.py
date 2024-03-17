from django.db import models


class Subscription(models.Model):
    """
    Subscription model
    """
    merchant_id = models.CharField(max_length=50)
    merchant_subscription_id = models.CharField(max_length=50)
    merchant_user_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_workflow_type = models.CharField(max_length=20)
    amount_type = models.CharField(max_length=10)
    amount = models.IntegerField()
    frequency = models.CharField(max_length=20)
    recurring_count = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    state = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions_table'


class AuthInit(models.Model):
    """
    AuthInit model
    """
    merchant_id = models.CharField(max_length=50)
    merchant_user_id = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=50)
    auth_req_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    subscription_flow_type = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_init_table'


class Transaction(models.Model):
    """
    Transaction model
    """
    merchant_id = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=50)
    auth_req_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    state = models.CharField(max_length=20)
    pay_response_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_table'



