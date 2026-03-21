from django.urls import path
from . import views

urlpatterns = [
    path('deliveries/', views.all_deliveries, name="deliveries"),
]