from django.utils import timezone

from deliverymanager.models import Route
from deliverymanager.models import Driver
from deliverymanager.models import Delivery

from deliverymanager.commands.delivery_command import DeliveryCommand


class GenerateRouteCommand(DeliveryCommand):
    def __init__(self, delivery_repository, routing_service):
        self.delivery_repository = delivery_repository
        self.routing_service = routing_service

    def execute(self, origin, driver_id):
        deliveries = list(self.delivery_repository.get_unassigned_deliveries())

        now = timezone.now()
        eligible_deliveries = []

        for delivery in deliveries:
            scheduled_time = getattr(delivery, "scheduled_time", None)

            # Normal deliveries won't have scheduled_time, so they remain eligible.
            # Custom deliveries only become eligible once their scheduled time arrives.
            if scheduled_time is not None and scheduled_time > now:
                continue

            eligible_deliveries.append(delivery)

        if not eligible_deliveries:
            return None

        driver = Driver.objects.get(id=driver_id)

        if driver.route is not None:
            raise ValueError(f"Driver '{driver.name}' already has an assigned route.")

        ordered_route_data = self.routing_service.get_ordered_route(origin, eligible_deliveries)
        totals = self.routing_service.calculate_totals(ordered_route_data)

        route = Route.objects.create(
            total_time=totals["total_duration_seconds"],
            total_distance=totals["total_distance_meters"]
        )

        driver.route = route
        driver.save()

        for index, stop in enumerate(ordered_route_data, start=1):
            delivery = stop["delivery"]
            delivery.route = route
            delivery.status = Delivery.STATUS_ASSIGNED
            delivery.route_order = index
            delivery.leg_distance_meters = stop["distance_meters"]

            duration_str = stop.get("duration")
            duration_seconds = None

            if isinstance(duration_str, str) and duration_str.endswith("s"):
                try:
                    duration_seconds = int(float(duration_str[:-1]))
                except ValueError:
                    duration_seconds = None

            delivery.leg_duration_seconds = duration_seconds
            delivery.save()

        return {
            "route": route,
            "driver": driver,
            "ordered_stops": ordered_route_data,
            "totals": totals
        }