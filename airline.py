from typing import List
from flight import Flight


class AirLine:
    def __init__(self, name: str):
        # Initialize the airline with a name and an empty list of flights
        self._name: str = name
        self._flights: List[Flight] = []

    @property
    def name(self):
        # Getter for the airline's name
        return self._name

    def get_flights(self):
        # Returns a copy of the list of flights to prevent external modifications
        return self._flights.copy()

    def add_flight(self, flight: Flight):
        # Adds a new flight to the list of flights
        self._flights.append(flight)

    def remove_flight_by_index(self, idx: int):
        # Removes a flight by index if it is within valid range
        if not (0 < idx <= len(self._flights)):
            raise ValueError("Invalid flight")
        del self._flights[idx]

    def remove_flight_object(self, flight: Flight):
        # Removes a flight by its object reference
        self._flights.remove(flight)
