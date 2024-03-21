from django.db import models

# Create your models here.
class Notification(models.Model):
    merchant_id = models.CharField(max_length=20)
    merchant_user_id = models.CharField(max_length=20)
    subscription_id = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    auto_debit = models.BooleanField(default=False)
    state = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications_table'