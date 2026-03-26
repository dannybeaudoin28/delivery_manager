import os
import requests


class RoutingService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("routes-api-key")
        self.routes_group_api_url = os.getenv("routes-group-api-url")
        
        print(self.routes_group_api_url)

        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "originIndex,destinationIndex,distanceMeters,duration,status,condition"
        }

   
    def get_multiple_routes(self, origin, deliveries):
        if not self.routes_group_api_url:
            raise ValueError("ROUTES_GROUP_API_URL is not set.")

        if not self.api_key:
            raise ValueError("ROUTES_API_KEY is not set.")

        body = {
            "origins": [
                {
                    "waypoint": {
                        "location": {
                            "latLng": {
                                "latitude": origin[0],
                                "longitude": origin[1]
                            }
                        }
                    }
                }
            ],
            "destinations": [],
            "travelMode": "DRIVE"
        }

        for delivery in deliveries:
            body["destinations"].append({
                "waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": delivery.latitude,
                            "longitude": delivery.longitude
                        }
                    }
                }
            })

        response = requests.post(
            url=self.routes_group_api_url,
            headers=self.headers,
            json=body,
            timeout=15
        )

        if response.status_code != 200:
            raise ValueError(
                f"Routing API error {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError:
            raise ValueError(f"Invalid JSON response from routing API: {response.text}")

    def get_ordered_route(self, origin, deliveries):
        current_location = origin
        remaining_stops = list(deliveries)
        ordered_route = []

        while remaining_stops:
            matrix = self.get_multiple_routes(current_location, remaining_stops)

            if not isinstance(matrix, list):
                raise ValueError(f"Unexpected route matrix format: {matrix}")

            candidates = []

            for elem in matrix:
                if not isinstance(elem, dict):
                    continue

                if elem.get("condition") != "ROUTE_EXISTS":
                    continue

                dist = elem.get("distanceMeters")
                if dist is None:
                    continue

                try:
                    distance_m = int(dist)
                    dest_idx = elem["destinationIndex"]
                    duration = elem.get("duration")
                    candidates.append((distance_m, dest_idx, duration))
                except (ValueError, KeyError, TypeError):
                    continue

            if not candidates:
                break

            highest_priority = min(
                self.get_delivery_priority(remaining_stops[candidate[1]])
                for candidate in candidates
            )

            priority_candidates = [
                candidate for candidate in candidates
                if self.get_delivery_priority(remaining_stops[candidate[1]]) == highest_priority
            ]

            best_distance, best_index, best_duration = min(priority_candidates, key=lambda t: t[0])

            next_stop = remaining_stops[best_index]

            ordered_route.append({
                "delivery": next_stop,
                "distance_meters": best_distance,
                "duration": best_duration,
            })

            current_location = (next_stop.latitude, next_stop.longitude)
            remaining_stops.pop(best_index)

        return ordered_route

    def calculate_totals(self, ordered_route):
        total_distance = 0
        total_duration_seconds = 0

        for stop in ordered_route:
            total_distance += stop.get("distance_meters", 0)

            duration = stop.get("duration")
            if isinstance(duration, str) and duration.endswith("s"):
                try:
                    total_duration_seconds += int(duration[:-1])
                except ValueError:
                    pass

        return {
            "total_distance_meters": total_distance,
            "total_duration_seconds": total_duration_seconds
        }
        
    def get_delivery_priority(self, delivery):
        return getattr(delivery, "priority_level", 3)