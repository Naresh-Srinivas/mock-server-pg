from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSubscriptionView.as_view(), name='create'),
    path('fetch_subscriptions/', views.FetchSubscriptionView.as_view(), name='fetchSubscription')
]