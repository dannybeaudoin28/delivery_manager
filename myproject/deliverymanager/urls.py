from django.urls import path
from . import views

urlpatterns = [
    path('all_deliveries', views.all_deliveries, name="deliveries"),
]