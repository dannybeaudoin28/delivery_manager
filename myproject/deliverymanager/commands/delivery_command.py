from abc import ABC, abstractmethod

class DeliveryCommand(ABC):

    def __init__(self, delivery_repository, geocoding_service):
        self.delivery_repository = delivery_repository
        self.geocoding_service = geocoding_service

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass