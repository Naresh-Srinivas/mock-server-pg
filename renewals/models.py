from django.db import models


# Create your models here.
class Renewal(models.Model):
    """
    Renewal Model
    """
    merchant_id = models.CharField(max_length=20)
    merchant_user_id = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=20)
    subscription_id = models.CharField(max_length=20)
    notification_id = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'renewals_debit_execute_table'
