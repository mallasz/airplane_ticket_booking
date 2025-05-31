from ticket_manager import TicketManager
from ticket_reservation import TicketReservation
from flight import Flight
from flight_factory import FlightFactory
from airline import AirLine

# Singleton instance that manages all airlines, flights, and reservations
ticket_manager = TicketManager()

# Utility input function for integer values with optional validation
def input_integer(question: str, validator: callable = None, invalid_text: str = "") -> int:
    while True:
        try:
            result = int(input(question + " "))
            if validator is None or validator(result):
                return result
            else:
                print(invalid_text)
        except ValueError:
            print(invalid_text)

# Utility input function for float values with optional validation
def input_float(question: str, validator: callable = None, invalid_text: str = "") -> float:
    while True:
        try:
            result = float(input(question + " "))
            if validator is None or validator(result):
                return result
            else:
                print(invalid_text)
        except ValueError:
            print(invalid_text)

# Utility input function for string values with optional validation
def input_string(question: str, validator: callable = None, invalid_text: str = "") -> str:
    while True:
        result = input(question + " ")
        if validator is None or validator(result):
            return result
        else:
            print(invalid_text)

# Main menu loop
def main_menu():
    while True:
        print()
        print("Main menu. The following functions are available:")
        print("1: Manage airlines")
        print("2: Manage flights")
        print("3: Manage ticket reservations")
        print("4: Manage files")
        print("0: Exit program")
        choice = input_integer("Choose a number!", lambda x: 0 <= x <= 4,
                               "The number must be an integer and between 0 and 4!")
        if choice == 0:
            return True
        elif choice == 1:
            handle_airlines()
        elif choice == 2:
            handle_flights()
        elif choice == 3:
            handle_tickets()
        elif choice == 4:
            handle_files()

# Submenu for managing airlines
def handle_airlines():
    while True:
        print()
        print("Airline menu. The following functions are available:")
        print("These are the known airlines:")
        for airline_name in ticket_manager.get_all_airlines().keys():
            print(f"  {airline_name}")
        print("1: Create new airline")
        print("2: Delete airline")
        print("0: Go back")
        choice = input_integer("Choose a number!", lambda x: 0 <= x <= 2,
                               "The number must be an integer and between 0 and 2!")
        if choice == 0:
            return
        elif choice == 1:
            create_airline()
        elif choice == 2:
            delete_airline()

# Create and add a new airline
def create_airline():
    print("Please enter a name for the new airline. A new airline will be created by that name.")
    name = input_string("name:", lambda s: s != "", "Be a bit more creative!")
    airline = AirLine(name)
    ticket_manager.add_airline(airline)

# Displays and lets the user choose an airline from the list
def choose_airline() -> None | AirLine:
    airlines = ticket_manager.get_all_airlines()
    for number, name in enumerate(airlines.keys(), 1):
        print(f"{number}: {name}")
    choice = input_integer("Choose a number!", lambda x: 0 <= x <= len(airlines),
                           "The number must be an integer from the left column!")
    if choice == 0:
        return None
    else:
        return list(airlines.values())[choice - 1]

# Delete a selected airline if it has no flights
def delete_airline():
    print("You can delete an airline. Please enter a valid number:")
    print("0: Cancel deletion and go back")
    airline = choose_airline()
    if airline is None:
        return
    try:
        ticket_manager.remove_airline_by_airline_object(airline)
    except ValueError as err:
        print(err)

# Lists all available flights grouped by airline
def list_flights():
    print("Currently available flights:")
    all_flights = ticket_manager.get_all_flights()
    i = 0
    for airline_name, flights in all_flights.items():
        print(f"{airline_name}: ")
        for flight in flights:
            i += 1
            print(f"  {i}: {flight}")

# Submenu for managing flights
def handle_flights():
    while True:
        print()
        print("Flight menu. The following functions are available:")
        print("1: List flights")
        print("2: Create new flight")
        print("3: Delete flight")
        print("4: Change flight's price")
        print("0: Go back")
        choice = input_integer("Choose a number!", lambda x: 0 <= x <= 4,
                               "The number must be an integer and between 0 and 4!")
        if choice == 0:
            return
        elif choice == 1:
            list_flights()
        elif choice == 2:
            create_flight()
        elif choice == 3:
            delete_flight()
        elif choice == 4:
            change_flight_price()

# Create a new flight (domestic or international) and add to selected airline
def create_flight():
    print("First, you need to choose an airline. Press 0 to cancel:")
    airline = choose_airline()
    if airline is None:
        return
    domestic_or_int_choice = input_integer("Is this new flight international (1) or domestic (2)? 0 to cancel.",
                                           lambda x: 0 <= x <= 2,
                                           "0: cancel, 1: international, 2: domestic")
    if domestic_or_int_choice == 0:
        return

    flight_number = input_string("Please enter a flight number:")
    destination = input_string("Enter a destination:")
    distance = input_float("What is the flight distance? Enter length in kilometres:",
                           lambda x: x > 0, "Flight must be longer than that!")
    price = input_float("Please enter ticket price. If you enter 0, the price will be calculated from flight distance.",
                        lambda x: x >= 0, "Price must be a nonnegative number")
    if price == 0.0:
        price = None

    flight_factory = FlightFactory()
    type_string = "domestic" if domestic_or_int_choice == 2 else "international"
    flight: Flight = flight_factory.create_flight(type_string, flight_number, destination, distance, price)
    airline.add_flight(flight)
    print("The price is {price}.")

# Let the user choose a flight from the selected airline
def choose_flight(airline: AirLine):
    print(f"Available flights for {airline.name}: ")
    print("0: Cancel")
    flights = airline.get_flights()
    for number, flight in enumerate(flights, 1):
        print(f"{number}: {flight}")
    choice = input_integer("Choose a number!", lambda x: 0 <= x <= len(flights),
                           "The number must be an integer from the left column!")
    if choice == 0:
        return None
    else:
        return flights[choice - 1]

# Delete a selected flight and also remove all associated reservations
def delete_flight():
    print("First, you need to choose an airline. Press 0 to cancel:")
    airline = choose_airline()
    if airline is None:
        return
    flight = choose_flight(airline)
    if flight is None:
        return
    airline.remove_flight_object(flight)
    reservations_to_be_deleted = [ticket for ticket in ticket_manager.get_all_tickets() if ticket.flight == flight]
    for ticket in reservations_to_be_deleted:
        ticket_manager.remove_ticket_by_ticket_object(ticket)

# Change the price of an existing flight
def change_flight_price():
    print("First, you need to choose an airline. Press 0 to cancel:")
    airline = choose_airline()
    if airline is None:
        return
    flight = choose_flight(airline)
    if flight is None:
        return
    price = input_float("Please enter ticket price. If you enter 0, the price will be calculated from flight distance.",
                        lambda x: x >= 0, "Price must be a non-negative number")
    if price == 0.0:
        price = flight.calculate_price(flight.distance)
    flight.price = price

# Submenu for ticket reservations
def handle_tickets():
    while True:
        print()
        print("Ticket menu. The following functions are available:")
        print("1: List ticket reservations")
        print("2: Create new ticket reservation")
        print("3: Delete reservation")
        print("0: Go back")
        choice = input_integer("Choose a number!", lambda x: 0 <= x <= 3,
                               "The number must be an integer and between 0 and 3!")
        if choice == 0:
            return
        elif choice == 1:
            list_tickets()
        elif choice == 2:
            create_ticket()
        elif choice == 3:
            delete_ticket()

# Display all ticket reservations
def list_tickets():
    tickets = ticket_manager.get_all_tickets()
    for number, ticket in enumerate(tickets, 1):
        print(f"{number}: {ticket}")

# Let the user choose a ticket from the list
def choose_ticket():
    print(f"Available tickets: ")
    print("0: Cancel")
    tickets = ticket_manager.get_all_tickets()
    for number, ticket in enumerate(tickets, 1):
        print(f"{number}: {ticket}")
    choice = input_integer("Choose a number!", lambda x: 0 <= x <= len(tickets),
                           "The number must be an integer from the left column!")
    if choice == 0:
        return None
    else:
        return tickets[choice - 1]

# Create a new ticket reservation for a passenger
def create_ticket():
    print("This creates a reservation. You can cancel this process by entering 0 at any point.")
    print("First you need to choose an airline to choose a flight:")
    airline = choose_airline()
    if airline is None:
        return
    flight = choose_flight(airline)
    if flight is None:
        return
    name = input_string("Now enter the passenger's name. The ticket will be created for that person.",
                        lambda s: s != "", "Please enter a name.")
    if name == "0":
        return
    ticket = TicketReservation(name, flight, flight.price)
    ticket_manager.add_ticket(ticket)

# Delete a selected ticket reservation
def delete_ticket():
    ticket = choose_ticket()
    if ticket is None:
        return
    ticket_manager.remove_ticket_by_ticket_object(ticket)

# File-related actions: save/load/reset data
def handle_files():
    while True:
        print()
        print("File menu. The following functions are available:")
        print("1: Save")
        print("2: Load")
        print("3: Restore default state")
        print("0: Go back")
        choice = input_integer("Choose a number!", lambda x: 0 <= x <= 3,
                               "The number must be an integer and between 0 and 3!")
        if choice == 0:
            return
        elif choice == 1:
            ticket_manager.save_state()
        elif choice == 2:
            ticket_manager.load_state()
        elif choice == 3:
            ticket_manager.load_default()

# Main function to start the program
def console_main():
    print("Hello! Welcome to my ticket booking software!")
    while True:
        try:
            res = main_menu()
            if res:
                return
        except KeyboardInterrupt:
            print("Function aborted. Return to main menu.")

# Start program when run directly
if __name__ == "__main__":
    console_main()
