from django.urls import path
from . import views

urlpatterns = [
    path('execute/', views.RenewalsExecuteView.as_view(), name='debit_execute'),
    path('status_check/', views.RenewalsStatusCheckView.as_view(), name='status_check'),
    path('callback/', views.RenewalsCallbackView.as_view(), name='callback')
]