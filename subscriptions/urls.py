from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateSubscriptionView.as_view(), name='create')
]