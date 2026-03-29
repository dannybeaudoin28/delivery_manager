from deliverymanager.models import Route
from deliverymanager.models import Delivery

class RouteRepository:
    """
    Repository responsible for encapsulating all data access logic
    related to Route entities.

    This abstraction keeps ORM queries out of higher layers
    (e.g., views, commands) and centralizes route-related queries.
    """

    def create_route(self, totals):
        """
        Create and persist a new Route using aggregated totals.

        Args:
            totals (dict): Dictionary containing route metrics such as:
                - total_duration_seconds
                - total_distance_meters

        Returns:
            Route: The newly created Route instance.
        """
        return Route.objects.create(
            total_time=totals["total_duration_seconds"],
            total_distance=totals["total_distance_meters"],
        )
        
    def get_latest_route_ordered_by_id_des(self):
        """
        Retrieve the most recently created Route based on descending ID.

        Returns:
            Route | None: The latest Route if it exists, otherwise None.
        """
        return Route.objects.order_by('-id').first()

    def get_all_routes_ordered_by_route_order(self, route):
        """
        Retrieve all deliveries associated with a given route,
        ordered by their route sequence.

        Args:
            route (Route): The route whose deliveries are being retrieved.

        Returns:
            QuerySet: Deliveries ordered by 'route_order'.
        """
        return route.deliveries.all().order_by('route_order')
    
    def count_remaining_deliveries(self, route):
        """
        Count the number of deliveries on a route that are still assigned
        (i.e., not yet completed).

        Args:
            route (Route): The route to inspect.
        Returns:
            int: Number of deliveries with STATUS_ASSIGNED.
        """
        return route.deliveries.filter(
            status=Delivery.STATUS_ASSIGNED
        ).count()