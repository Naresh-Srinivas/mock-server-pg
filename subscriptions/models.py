from django.db import models


class Subscription(models.Model):
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
