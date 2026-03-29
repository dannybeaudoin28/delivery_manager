import os
import geocoder

class GeocodingService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ROUTES_API_KEY")

    def get_coordinates(self, address):
        geo = geocoder.google(address, key=self.api_key)

        if not geo.ok or not geo.latlng:
            raise ValueError(f"Could not geocode address: {address}")

        lat, lng = geo.latlng
        return lat, lng