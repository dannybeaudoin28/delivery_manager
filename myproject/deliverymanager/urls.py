from django.contrib import admin


from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('add-delivery', views.add_delivery_view, name='add_delivery'),
    path('deliveries/delete/<int:delivery_id>/', views.remove_delivery_view, name='remove_delivery'),
    path('deliveries/clear-queue', views.clear_queue_view, name='clear_queue'),
    path('generate-route/', views.generate_route_view, name='generate_route'),
    path(
        'deliveries/<int:delivery_id>/mark-delivered/',
        views.mark_delivered,
        name='mark_delivery_delivered'
    ),
    path('delivery/<int:delivery_id>/edit/', views.edit_delivery, name='edit_delivery'),
]