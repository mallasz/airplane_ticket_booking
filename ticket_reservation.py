from flight import Flight


# Represents a ticket reservation made by a passenger for a specific flight
class TicketReservation:
    def __init__(self, name: str, flight: Flight, price: float):
        self.name: str = name       # Name of the passenger
        self.flight = flight        # Flight object the ticket is for
        self.price = price          # Final ticket price at the time of reservation

    def __str__(self):
        # Returns a readable string representation of the reservation
        return f"TicketReservation {self.name=} {self.flight=} {self.price=}"
