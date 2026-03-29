import os
import geocoder


class GeocodingService:
    """
    Service responsible for converting addresses into geographic coordinates.

    Wraps the external geocoding API to keep third-party logic isolated
    from the rest of the application.
    """

    def __init__(self, api_key=None):
        """
        Initialize the service with an API key.

        Args:
            api_key (str, optional): API key for the geocoding service.
                                     Falls back to environment variable if not provided.
        """
        self.api_key = api_key or os.getenv("ROUTES_API_KEY")

    def get_coordinates(self, address):
        """
        Convert a human-readable address into latitude and longitude.

        Args:
            address (str): The address to geocode.

        Returns:
            tuple: (latitude, longitude)

        Raises:
            ValueError: If the address cannot be geocoded.
        """
        # Call external geocoding API
        geo = geocoder.google(address, key=self.api_key)

        # Validate response
        if not geo.ok or not geo.latlng:
            raise ValueError(f"Could not geocode address: {address}")

        # Extract and return coordinates
        lat, lng = geo.latlng
        return lat, lng