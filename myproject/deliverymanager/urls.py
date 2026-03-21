from django.urls import path
from . import views

urlpatterns = [
    path('add-delivery/', views.add_delivery_view, name="add_delivery"),
    path('deliveries/', views.delivery_list_view, name="delivery_list"),
]