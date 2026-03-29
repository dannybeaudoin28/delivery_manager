from abc import ABC, abstractmethod
from typing import Any

class DeliveryCommand(ABC):
    """
    Abstract base class for all delivery-related commands.

    Concrete command classes encapsulate a single application action
    such as adding, updating, deleting, or routing deliveries.
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the command.

        Concrete subclasses must implement this method.
        """
        pass