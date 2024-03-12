from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSubscriptionView.as_view(), name='create'),
    path('fetchSubscription/', views.FetchSubscriptionView.as_view(), name='fetchSubscription')
]