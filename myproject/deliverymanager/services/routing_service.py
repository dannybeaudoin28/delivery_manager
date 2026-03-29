import os
import requests


class RoutingService:
    """
    Service responsible for interacting with the Google Routes API
    and computing optimized delivery routes.
    """

    def __init__(self, api_key=None):
        """
        Initialize routing service with API credentials and headers.
        """
        self.api_key = api_key or os.getenv("ROUTES_API_KEY")
        self.routes_group_api_url = os.getenv("ROUTES_GROUP_API_URL")
        
        # Predefine headers for all API requests
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "originIndex,destinationIndex,distanceMeters,duration,status,condition"
        }

   
    def get_multiple_routes(self, origin, deliveries):
        """
        Call the route matrix API to compute distances and durations
        from a single origin to multiple delivery destinations.
        """
        # Validate required configuration
        if not self.routes_group_api_url:
            raise ValueError("ROUTES_GROUP_API_URL is not set.")

        if not self.api_key:
            raise ValueError("ROUTES_API_KEY is not set.")

        # Build request body
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

        # Add all delivery destinations
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

        # Send request to routing API
        response = requests.post(
            url=self.routes_group_api_url,
            headers=self.headers,
            json=body,
            timeout=15
        )

        # Handle API errors
        if response.status_code != 200:
            raise ValueError(
                f"Routing API error {response.status_code}: {response.text}"
            )

        # Parse JSON response
        try:
            return response.json()
        except ValueError:
            raise ValueError(f"Invalid JSON response from routing API: {response.text}")

    def get_ordered_route(self, origin, deliveries):
        """
        Generate an ordered route using a greedy approach:
        repeatedly select the closest (and highest priority) next stop.
        """
        current_location = origin
        remaining_stops = list(deliveries)
        ordered_route = []

        # Continue until all deliveries are processed
        while remaining_stops:
            matrix = self.get_multiple_routes(current_location, remaining_stops)

            if not isinstance(matrix, list):
                raise ValueError(f"Unexpected route matrix format: {matrix}")

            candidates = []

            # Extract valid route candidates
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

            # Determine highest priority among candidates (lower = higher priority)
            highest_priority = min(
                self.get_delivery_priority(remaining_stops[candidate[1]])
                for candidate in candidates
            )

            # Filter candidates by priority
            priority_candidates = [
                candidate for candidate in candidates
                if self.get_delivery_priority(remaining_stops[candidate[1]]) == highest_priority
            ]

            # Select closest candidate among highest priority deliveries
            best_distance, best_index, best_duration = min(priority_candidates, key=lambda t: t[0])

            next_stop = remaining_stops[best_index]

            ordered_route.append({
                "delivery": next_stop,
                "distance_meters": best_distance,
                "duration": best_duration,
            })

            # Update current location and remaining stops
            current_location = (next_stop.latitude, next_stop.longitude)
            remaining_stops.pop(best_index)

            # After final stop, compute return-to-origin leg
            if ordered_route:
                last_stop = ordered_route[-1]["delivery"]
                last_location = (last_stop.latitude, last_stop.longitude)

                # Lightweight object to represent origin as a destination
                class RoutePoint:
                    def __init__(self, latitude, longitude):
                        self.latitude = latitude
                        self.longitude = longitude

                home_stop = RoutePoint(origin[0], origin[1])

                return_matrix = self.get_multiple_routes(last_location, [home_stop])

                for elem in return_matrix:
                    if not isinstance(elem, dict):
                        continue

                    if elem.get("condition") != "ROUTE_EXISTS":
                        continue

                    dist = elem.get("distanceMeters")
                    if dist is None:
                        continue

                    try:
                        distance_m = int(dist)
                        duration = elem.get("duration")

                        ordered_route.append({
                            "delivery": None,
                            "distance_meters": distance_m,
                            "duration": duration,
                            "is_return": True
                        })

                        break
                    except (ValueError, TypeError):
                        continue
        
        return ordered_route

    def calculate_totals(self, ordered_route):
        """
        Calculate total distance and duration from an ordered route.
        """
        total_distance = 0
        total_duration_seconds = 0

        for stop in ordered_route:
            total_distance += stop.get("distance_meters", 0)

            duration = stop.get("duration")
            # Convert duration string (e.g., "120s") to integer seconds
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
        """
        Return delivery priority, defaulting to 3 if not specified.
        """
        return getattr(delivery, "priority_level", 3)