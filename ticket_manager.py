from typing import List, Dict
import pickle

import metaclasses
from airline import AirLine
from flight import Flight
from ticket_reservation import TicketReservation


# The TicketManager handles all airlines, flights, and ticket reservations.
# It uses the Singleton metaclass to ensure only one instance exists.
class TicketManager(metaclass=metaclasses.Singleton):

    FILE_NAME: str = "tickets.pickle"         # Default filename for saving state
    DEFAULT_NAME: str = "default.pickle"      # Default file to load initial state from

    def __init__(self):
        # List of airlines and ticket reservations in memory
        self.airlines: List[AirLine] = []
        self.tickets: List[TicketReservation] = []
        # Load initial data
        self.load_default()

    # Returns a dictionary of all airlines by name
    def get_all_airlines(self):
        return {airline.name: airline for airline in self.airlines}

    # Returns a dictionary of all flights grouped by airline name
    def get_all_flights(self) -> Dict[str, List[Flight]]:
        return {airline.name: airline.get_flights() for airline in self.airlines}

    # Returns a copy of all current ticket reservations
    def get_all_tickets(self) -> List[TicketReservation]:
        return self.tickets.copy()

    # Adds a ticket to the system
    def add_ticket(self, ticket: TicketReservation) -> bool:
        if ticket is None:
            return False
        self.tickets.append(ticket)
        return True

    # Removes a ticket by its index in the list and returns the refunded price
    def remove_ticket_by_index(self, idx: int) -> float:
        if idx < 0 or idx >= len(self.tickets):
            raise ValueError("Wrong index")
        ticket: TicketReservation = self.tickets[idx]
        return self.remove_ticket_by_ticket_object(ticket)

    # Removes a ticket by reference and returns the refunded price
    def remove_ticket_by_ticket_object(self, ticket: TicketReservation) -> float:
        refund: float = ticket.price
        self.tickets.remove(ticket)
        return refund

    # Adds a new airline to the system
    def add_airline(self, airline: AirLine):
        self.airlines.append(airline)

    # Removes an airline, but only if it has no flights
    def remove_airline_by_airline_object(self, airline):
        if len(airline.get_flights()) > 0:
            raise ValueError("Airline must be empty")
        self.airlines.remove(airline)

    # Creates and adds a new ticket reservation
    def create_reservation(self, real_name: str, flight: Flight) -> float:
        ticket = TicketReservation(real_name, flight, flight.price)
        self.add_ticket(ticket)
        return ticket.price

    # Saves the current state (airlines and tickets) to a file
    def save_state(self):
        with open(self.FILE_NAME, 'wb') as f:
            data = {
                "airlines": self.airlines,
                "tickets": self.tickets
            }
            pickle.dump(data, f)

    # Loads the system state from a file
    def load_state(self, file_name=None) -> bool:
        if file_name is None:
            file_name = self.FILE_NAME
        try:
            with open(file_name, 'rb') as f:
                pickle_content = pickle.load(f)
            if isinstance(pickle_content, dict):
                self.airlines = pickle_content.get("airlines", self.airlines)
                self.tickets = pickle_content.get("tickets", self.tickets)
                return True
        except FileNotFoundError:
            return False

    # Loads the default saved state from DEFAULT_NAME file
    def load_default(self):
        self.load_state(self.DEFAULT_NAME)
