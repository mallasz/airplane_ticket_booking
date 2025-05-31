from typing import Optional
from flight import Flight


class InternationalFlight(Flight):
    def __init__(self, flight_number: str, destination: str, distance: float, price: Optional[float] = None):
        # Initialize an international flight using the base Flight class
        super().__init__(flight_number, destination, distance, price)

    def calculate_price(self, distance):
        # Calculates ticket price for international flights (higher rate per km)
        return distance * 12.0

    def __str__(self):
        # User-friendly string representation of the international flight
        return f"InternationalFlight[{self.flight_number=} {self.destination=} {self.distance=} {self.price=}]"

    def __repr__(self):
        # Developer-friendly representation (same as __str__ here)
        return self.__str__()

    def is_international(self):
        # Returns True because this is an international flight
        return True
