from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('create/', views.CreateNotificationView.as_view(), name=''),
    path('status_check/', views.StatusNotificationView.as_view(), name='status'),
    path('callback/', views.CallbackNotificationView.as_view(), name='callback')
]