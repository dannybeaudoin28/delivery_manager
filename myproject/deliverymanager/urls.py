from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add-delivery/', views.add_delivery_view, name='add_delivery'),
    path('deliveries/delete/<int:delivery_id>/', views.remove_delivery_view, name='remove_delivery'),
]