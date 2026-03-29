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

# Instantiate repositories, services, and factory once for reuse across views
delivery_repository = DeliveryRepository()
driver_repository = DriverRepository()
routing_repository = RouteRepository()

geocoding_service = GeocodingService()
routing_service = RoutingService()

delivery_factory = DeliveryFactory()


def dashboard_view(request):
    """
    Main dashboard view.

    Displays:
    - Unassigned deliveries
    - All deliveries
    - Available drivers
    - Latest generated route and its breakdown

    Also ensures drivers are unassigned from routes that no longer
    have active deliveries.
    """
    remaining_time = 0 
    distance = 0
    deliveries = delivery_repository.get_unassigned_deliveries()
    all_deliveries = delivery_repository.get_all_deliveries()
    null_routes = driver_repository.exclude_null_routes()
    
    # Clean up drivers whose routes no longer have active deliveries
    for driver in null_routes:
        route = driver.route
        if route is None:
            continue

        # Count active deliveries for this driver's route
        active_deliveries = delivery_repository.get_active_deliveries(route)  # type: ignore

        if active_deliveries == 0:
            driver.route = None
            driver_repository.save_driver(driver)

    # Retrieve available drivers and most recent route
    drivers = driver_repository.get_available_driver_ordered_by_name()    
    latest_route = routing_repository.get_latest_route_ordered_by_id_des()
    latest_route_deliveries = []
    latest_route_stops = []

    if latest_route:
        latest_route_deliveries = routing_repository.get_all_routes_ordered_by_route_order(latest_route)

        # Compute display-friendly time and distance values
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

        # Build a list of route stops including per-leg distance/duration
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

        # Add return-to-origin leg if applicable
        return_distance = latest_route.total_distance - total_delivery_distance
        return_duration = latest_route.total_time - total_delivery_duration

        if return_distance > 0 or return_duration > 0:
            latest_route_stops.append({
                "is_return": True,
                "delivery": None,
                "distance_meters": return_distance,
                "duration_seconds": return_duration,
            })

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
    """
    View showing only unassigned deliveries.
    """
    deliveries = delivery_repository.get_unassigned_deliveries()
    
    return render(request, "deliverymanager/delivery_list.html", {
        "deliveries": deliveries
    })


from datetime import datetime

def add_delivery_view(request):
    """
    Handles creation of a new delivery.

    Supports both:
    - Normal deliveries
    - Custom deliveries (priority + scheduled time)

    Delegates creation logic to AddDeliveryCommand.
    """
    if request.method == "POST":
        address = request.POST.get("address")
        delivery_type = request.POST.get("delivery_type", "normal")

        command = AddDeliveryCommand(
            geocoding_service,
            delivery_repository,
            delivery_factory
        )

        # Prepare arguments for command execution
        kwargs = {
            "address": address,
            "delivery_type": delivery_type,
        }

        # Handle additional fields for custom deliveries
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
    """
    Clears all unassigned deliveries from the queue.
    """
    if request.method == "POST":
        delivery_repository.clear_queue()
    return redirect('dashboard')


def generate_route_view(request):
    """
    Generates an optimized delivery route for a selected driver.

    Delegates route computation and assignment to GenerateRouteCommand.
    """
    if request.method == "POST":
        try:
            driver_id = request.POST.get("driver_id")

            if not driver_id:
                return HttpResponse("Please select a driver.", status=400)

            command = GenerateRouteCommand(delivery_repository, driver_repository, routing_repository, routing_service)

            origin = (44.2312, -76.4860)
            command.execute(origin, driver_id)

        except Exception as e:
            return HttpResponse(f"Route generation failed: {e}", status=500)

    return redirect("dashboard")


def mark_delivered(request, delivery_id):
    """
    Marks a delivery as delivered and updates route/driver state
    accordingly via MarkDeliveryDeliveredCommand.
    """
    if request.method == "POST":
        command = MarkDeliveryDeliveredCommand(
                driver_repository,
                delivery_repository,
                routing_repository
            )
        
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
    delivery = delivery_repository.get_delivery_by_id(delivery_id)

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