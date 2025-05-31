from typing import Optional
from flight import Flight


class DomesticFlight(Flight):
    def __init__(self, flight_number: str, destination: str, distance: float, price: Optional[float] = None):
        # Initialize a domestic flight using the base Flight class
        super().__init__(flight_number, destination, distance, price)

    def calculate_price(self, distance):
        # Calculates ticket price for domestic flights (fixed rate per km)
        return distance * 10.0

    def __str__(self):
        # User-friendly string representation of the domestic flight
        return f"DomesticFlight[{self.flight_number=} {self.destination=} {self.distance=} {self.price=}]"

    def __repr__(self):
        # Developer-friendly representation (same as __str__ here)
        return self.__str__()

    def is_international(self):
        # Returns False because this is a domestic flight
        return False
