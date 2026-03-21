from django.shortcuts import render, redirect
from django.http import HttpResponse

from deliverymanager.commands.add_delivery_command import AddDeliveryCommand
from deliverymanager.repositories.delivery_repository import DeliveryRepository
from deliverymanager.services.geocoding_service import GeocodingService

delivery_repository = DeliveryRepository()
geocoding_service = GeocodingService()

def delivery_list_view(request):
    deliveries = delivery_repository.get_unassigned_deliveries()
    
    return render(request, "deliverymanager/delivery_list.html", {
        "deliveries": deliveries
    })

def add_delivery_view(request):
    if request.method == "POST":
        address = request.POST.get("address")
        
        
        command = AddDeliveryCommand(delivery_repository, geocoding_service)
        
        command.execute(address)
        
        return redirect("delivery_list")
    return render(request, "deliverymanager/add_delivery.html")