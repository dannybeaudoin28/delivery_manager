from django.utils import timezone

from deliverymanager.models import Route
from deliverymanager.models import Driver
from deliverymanager.models import Delivery

from deliverymanager.commands.delivery_command import DeliveryCommand


class GenerateRouteCommand(DeliveryCommand):
    """
    Command responsible for generating and assigning an optimized route
    to a driver based on currently eligible deliveries.
    """

    def __init__(self, delivery_repository, routing_service):
        self.delivery_repository = delivery_repository
        self.routing_service = routing_service

    def execute(self, origin, driver_id):
        """
        Generate a route for a driver using all eligible unassigned deliveries.

        Args:
            origin (str): Starting address or origin for the route.
            driver_id (int): ID of the driver receiving the route.

        Returns:
            dict | None: Route result data, or None if no deliveries are eligible.
        """
        deliveries = list(self.delivery_repository.get_unassigned_deliveries())
        eligible_deliveries = self._get_eligible_deliveries(deliveries)

        if not eligible_deliveries:
            return None

        driver = self._get_available_driver(driver_id)
        ordered_route_data = self._generate_ordered_route(origin, eligible_deliveries)
        totals = self.routing_service.calculate_totals(ordered_route_data)

        route = self._create_route(totals)
        self._assign_route_to_driver(driver, route)
        self._assign_deliveries_to_route(route, ordered_route_data)

        return {
            "route": route,
            "driver": driver,
            "ordered_stops": ordered_route_data,
            "totals": totals,
        }

    def _get_eligible_deliveries(self, deliveries):
        """
        Return deliveries that are eligible to be routed.

        Normal deliveries are immediately eligible.
        Scheduled deliveries are only eligible once their scheduled time arrives.
        """
        now = timezone.now()
        eligible_deliveries = []

        for delivery in deliveries:
            scheduled_time = getattr(delivery, "scheduled_time", None)

            if scheduled_time is not None and scheduled_time > now:
                continue

            eligible_deliveries.append(delivery)

        return eligible_deliveries

    def _get_available_driver(self, driver_id):
        """
        Retrieve a driver and ensure they do not already have an assigned route.
        """
        driver = Driver.objects.get(id=driver_id)

        if driver.route is not None:
            raise ValueError(f"Driver '{driver.name}' already has an assigned route.")

        return driver

    def _generate_ordered_route(self, origin, eligible_deliveries):
        """
        Request an optimized route from the routing service.
        """
        ordered_route_data = self.routing_service.get_ordered_route(
            origin,
            eligible_deliveries
        )

        print("ORDERED ROUTE DATA:")
        for stop in ordered_route_data:
            print(stop)

        return ordered_route_data

    def _create_route(self, totals):
        """
        Create and persist a new Route record using calculated totals.
        """
        return Route.objects.create(
            total_time=totals["total_duration_seconds"],
            total_distance=totals["total_distance_meters"],
        )

    def _assign_route_to_driver(self, driver, route):
        """
        Assign the newly created route to the specified driver.
        """
        driver.route = route
        driver.save()

    def _assign_deliveries_to_route(self, route, ordered_route_data):
        """
        Assign each routed delivery to the route and store route leg metadata.
        """
        route_order = 1

        for stop in ordered_route_data:
            if stop.get("is_return"):
                continue

            delivery = stop["delivery"]
            delivery.route = route
            delivery.status = Delivery.STATUS_ASSIGNED
            delivery.route_order = route_order
            delivery.leg_distance_meters = stop["distance_meters"]
            delivery.leg_duration_seconds = self._parse_duration_to_seconds(
                stop.get("duration")
            )
            delivery.save()

            route_order += 1

    def _parse_duration_to_seconds(self, duration_str):
        """
        Convert a duration string like '120s' into an integer number of seconds.
        Returns None if parsing fails.
        """
        if isinstance(duration_str, str) and duration_str.endswith("s"):
            try:
                return int(float(duration_str[:-1]))
            except ValueError:
                return None

        return None