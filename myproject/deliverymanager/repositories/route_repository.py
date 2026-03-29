from deliverymanager.models import Route

class RouteRepository:
    
    def create_route(self, totals):
        return Route.objects.create(
            total_time=totals["total_duration_seconds"],
            total_distance=totals["total_distance_meters"],
        )
        
    def get_latest_route_ordered_by_id_des(self):
        return Route.objects.order_by('-id').first()

    def get_all_routes_ordered_by_route_order(self, route):
        return route.deliveries.all().order_by('route_order')