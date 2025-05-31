from abc import ABC, abstractmethod, abstractproperty
from typing import Optional

# Abstract base class representing a general flight
class Flight(ABC):
    def __init__(self, flight_number: str, destination: str, distance: float, price: Optional[float]=None):
        # Initialize flight attributes
        self._flight_number: str = flight_number      # Unique identifier for the flight
        self._destination: str = destination          # Destination city or airport
        self._distance: float = distance              # Distance of the flight in kilometers

        # If no price is provided, calculate it using the subclass's implementation
        if price is None:
            price = self.calculate_price(distance)
        self._price: float = price

    @abstractmethod
    def calculate_price(self, distance):
        # Abstract method to calculate the ticket price based on distance
        pass

    # Property for flight number
    @property
    def flight_number(self):
        return self._flight_number

    @flight_number.setter
    def flight_number(self, flight_number):
        self._flight_number = flight_number

    # Property for destination
    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination):
        self._destination = destination

    # Property for price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    # Property for distance
    @property
    def distance(self):
        return self._distance

    @abstractmethod
    def __str__(self):
        # Abstract method to provide a string representation of the flight
        pass

    @abstractmethod
    def is_international(self):
        # Abstract method to determine if the flight is international
        pass
