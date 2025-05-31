from typing import Optional

from flight import Flight
from international_flight import InternationalFlight
from domestic_flight import DomesticFlight
from metaclasses import Singleton


# Factory class for creating flight objects.
# Uses Singleton pattern to ensure only one instance of the factory exists.
class FlightFactory(metaclass=Singleton):

    def create_flight(self, kind: str, flight_number: str, destination: str, distance: float, price: Optional[float]=None) -> Flight:
        """
        Creates a flight instance based on the 'kind' parameter.

        Parameters:
        - kind: "international" or "domestic"
        - flight_number: identifier for the flight
        - destination: destination of the flight
        - distance: distance in kilometers
        - price: optional, calculated if not provided

        Returns:
        - An instance of InternationalFlight or DomesticFlight

        Raises:
        - ValueError if the flight type is unknown
        """
        kind = kind.lower()
        if kind == "international":
            return InternationalFlight(flight_number, destination, distance, price)
        if kind == "domestic":
            return DomesticFlight(flight_number, destination, distance, price)
        raise ValueError("Unknown flight type")
