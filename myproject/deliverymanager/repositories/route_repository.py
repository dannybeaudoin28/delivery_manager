from deliverymanager.models import Route

class RouteRepository:
    
    def create_route(self, totals):
        return Route.objects.create(
            total_time=totals["total_duration_seconds"],
            total_distance=totals["total_distance_meters"],
        )