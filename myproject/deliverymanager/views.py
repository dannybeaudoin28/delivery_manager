from django.shortcuts import render, redirect, get_object_or_404
from deliverymanager.models import Delivery
from django.http import HttpResponse

from deliverymanager.commands.add_delivery_command import AddDeliveryCommand
from deliverymanager.commands.generate_route_command import GenerateRouteCommand
from deliverymanager.commands.mark_delivery_delivered_command import MarkDeliveryDeliveredCommand
from deliverymanager.commands.remove_delivery_command import RemoveDeliveryCommand
from deliverymanager.commands.update_delivery_command import UpdateDeliveryCommand

from deliverymanager.repositories.delivery_repository import DeliveryRepository
from deliverymanager.repositories.driver_repository import DriverRepository
from deliverymanager.repositories.route_repository import RouteRepository


from deliverymanager.services.geocoding_service import GeocodingService
from deliverymanager.services.routing_service import RoutingService

from deliverymanager.models import Route
from deliverymanager.models import Driver

from deliverymanager.factories.delivery_factory import DeliveryFactory

from django.utils import timezone

delivery_repository = DeliveryRepository()
driver_repository = DriverRepository()
routing_repository = RouteRepository()

geocoding_service = GeocodingService()
routing_service = RoutingService()

delivery_factory = DeliveryFactory()

def dashboard_view(request):
    remaining_time = 0 
    distance = 0
    deliveries = delivery_repository.get_unassigned_deliveries()
    all_deliveries = delivery_repository.get_all_deliveries()
    
    for driver in Driver.objects.exclude(route__isnull=True):
        route = driver.route
        if route is None:
            continue

        active_deliveries = route.deliveries.filter(status=Delivery.STATUS_ASSIGNED).count() # type: ignore

        if active_deliveries == 0:
            driver.route = None
            driver.save()

    drivers = Driver.objects.filter(route__isnull=True).order_by("name")    
    latest_route = Route.objects.order_by('-id').first()
    latest_route_deliveries = []
    latest_route_stops = []

    if latest_route:
        latest_route_deliveries = latest_route.deliveries.all().order_by('route_order')

        minutes, seconds = divmod(latest_route.total_time, 60)
        kilometers, meters = divmod(latest_route.total_distance, 1000)

        remaining_time = {
            "quotient": minutes,
            "remainder": seconds
        }

        distance = {
            "quotient": kilometers,
            "remainder": meters
        }

        total_delivery_distance = 0
        total_delivery_duration = 0

        for delivery in latest_route_deliveries:
            leg_distance = delivery.leg_distance_meters or 0
            leg_duration = delivery.leg_duration_seconds or 0

            total_delivery_distance += leg_distance
            total_delivery_duration += leg_duration

            latest_route_stops.append({
                "is_return": False,
                "delivery": delivery,
                "distance_meters": leg_distance,
                "duration_seconds": leg_duration,
            })

        return_distance = latest_route.total_distance - total_delivery_distance
        return_duration = latest_route.total_time - total_delivery_duration

        if return_distance > 0 or return_duration > 0:
            latest_route_stops.append({
                "is_return": True,
                "delivery": None,
                "distance_meters": return_distance,
                "duration_seconds": return_duration,
            })
            
        print("ROUTE TOTAL DISTANCE:", latest_route.total_distance)
        print("SUM DELIVERY DISTANCE:", total_delivery_distance)
        print("RETURN DISTANCE:", return_distance)

        print("ROUTE TOTAL TIME:", latest_route.total_time)
        print("SUM DELIVERY TIME:", total_delivery_duration)
        print("RETURN TIME:", return_duration)

    return render(request, "deliverymanager/dashboard.html", {
        "deliveries": deliveries,
        "all_deliveries": all_deliveries,
        "latest_route": latest_route,
        "drivers": drivers,
        "latest_route_deliveries": latest_route_deliveries,
        "remaining_time": remaining_time,
        "distance": distance,
        "latest_route_stops": latest_route_stops,
    })

def delivery_list_view(request):
    deliveries = delivery_repository.get_unassigned_deliveries()
    
    return render(request, "deliverymanager/delivery_list.html", {
        "deliveries": deliveries
    })

from datetime import datetime

def add_delivery_view(request):
    if request.method == "POST":
        address = request.POST.get("address")
        delivery_type = request.POST.get("delivery_type", "normal")

        command = AddDeliveryCommand(
            geocoding_service,
            delivery_repository,
            delivery_factory
        )

        kwargs = {
            "address": address,
            "delivery_type": delivery_type,
        }

        if delivery_type == "custom":
            priority_level = request.POST.get("priority_level")
            scheduled_time = request.POST.get("scheduled_time")

            if priority_level:
                kwargs["priority_level"] = int(priority_level)

            if scheduled_time:
                naive_dt = datetime.fromisoformat(scheduled_time)
                aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
                kwargs["scheduled_time"] = aware_dt

        command.execute(**kwargs)

    return redirect("dashboard")

def remove_delivery_view(request, delivery_id):
    """
    Handle deletion of a delivery via POST request.
    Delegates deletion behavior to the RemoveDeliveryCommand.
    """
    if request.method == "POST":
        command = RemoveDeliveryCommand(delivery_repository)
        command.execute(delivery_id)

    return redirect("dashboard")

def clear_queue_view(request):
    if request.method == "POST":
        delivery_repository.clear_queue()
    return redirect('dashboard')

def generate_route_view(request):
    if request.method == "POST":
        try:
            driver_id = request.POST.get("driver_id")

            if not driver_id:
                return HttpResponse("Please select a driver.", status=400)

            routing_service = RoutingService()
            command = GenerateRouteCommand(delivery_repository, driver_repository, routing_repository, routing_service)

            origin = (44.2312, -76.4860)
            command.execute(origin, driver_id)

        except Exception as e:
            return HttpResponse(f"Route generation failed: {e}", status=500)

    return redirect("dashboard")

def mark_delivered(request, delivery_id):
    print("ID IS: " + str(delivery_id))
    if request.method == "POST":
        command = MarkDeliveryDeliveredCommand(delivery_repository)
        command.execute(delivery_id)

    return redirect("dashboard")

def edit_delivery(request, delivery_id):
    """
    Handle delivery edits.

    GET:
        Render the edit form.

    POST:
        Update the delivery using the UpdateDeliveryCommand and redirect
        back to the dashboard.
    """
    delivery = get_object_or_404(Delivery, id=delivery_id)

    if request.method == "POST":
        address = request.POST.get("address", "").strip()

        command = UpdateDeliveryCommand(
            delivery_repository,
            geocoding_service,
        )
        command.execute(delivery_id, address=address)

        return redirect("dashboard")

    return render(
        request,
        "deliverymanager/edit_delivery.html",
        {"delivery": delivery},
    )