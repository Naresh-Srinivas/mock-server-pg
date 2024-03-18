from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSubscriptionView.as_view(), name='create'),
    path('fetch_subscriptions/', views.FetchSubscriptionView.as_view(), name='fetchSubscription'),
    path('status_check/', views.StatusCheckView.as_view(), name='statusCheck'),
    path('auth/init/', views.AuthView.as_view(), name='authInit'),
    path('auth/status/', views.AuthStatusView.as_view(), name='authStatus'),
    path('transaction/', views.TransactionView.as_view(), name='transaction'),
    path('cancel/', views.CancelSubscriptionView.as_view(), name='cancel'),
    path('cancel/callback/', views.CancelCallbackView.as_view(), name='closeCallback')
]