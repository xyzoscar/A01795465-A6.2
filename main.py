"""
Hotel Reservation System

A console-based application for managing hotels, customers, and reservations.
Supports CRUD operations with data persistence in JSON files. Includes input
validation and basic error handling.
"""
import json
import re
from os import path


class Hotel:
    """Represents a hotel with basic operations and file persistence."""
    _file_path = 'hotels.json'

    def __init__(self, name, location, rooms_available, email):
        self.name = name
        self.location = location
        self.rooms_available = rooms_available
        self.email = email

    @classmethod
    def load_hotels(cls):
        """Load all hotels from JSON file."""
        try:
            if not path.exists(cls._file_path):
                return []
            with open(cls._file_path, 'r', encoding='utf-8') as f:
                return [cls(**hotel) for hotel in json.load(f)]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading hotels: {str(e)}")
            return []

    def save(self):
        """Save current hotel to persistent storage."""
        hotels = self.load_hotels()
        existing = next((h for h in hotels if h.name == self.name), None)
        if existing:
            hotels.remove(existing)
        hotels.append(self)
        self._save_all(hotels)

    @classmethod
    def _save_all(cls, hotels):
        """Save list of hotels to file."""
        try:
            with open(cls._file_path, 'w', encoding='utf-8') as f:
                json.dump([h.__dict__ for h in hotels], f)
        except IOError as e:
            print(f"Error saving hotels: {str(e)}")

    def delete(self):
        """Remove hotel from persistent storage."""
        hotels = self.load_hotels()
        hotels = [h for h in hotels if h.name != self.name]
        self._save_all(hotels)

    def reserve_room(self):
        """Decrease available room count by one."""
        if self.rooms_available > 0:
            self.rooms_available -= 1
            self.save()
            return True
        return False

    def cancel_reservation(self):
        """Increase available room count by one."""
        self.rooms_available += 1
        self.save()

    @classmethod
    def set_file_path(cls, new_path):
        """Set file path for testing purposes."""
        cls._file_path = new_path

    @classmethod
    def get_file_path(cls):
        """Get current file path."""
        return cls._file_path


class Customer:
    """Represents a customer with validation and file persistence."""
    _file_path = 'customers.json'

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    @classmethod
    def load_customers(cls):
        """Load all customers from JSON file."""
        try:
            if not path.exists(cls._file_path):
                return []
            with open(cls._file_path, 'r', encoding='utf-8') as f:
                return [cls(**customer) for customer in json.load(f)]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading customers: {str(e)}")
            return []

    def save(self):
        """Persist customer to storage."""
        customers = self.load_customers()
        existing = next((c for c in customers if c.email == self.email), None)
        if existing:
            customers.remove(existing)
        customers.append(self)
        self._save_all(customers)

    @classmethod
    def _save_all(cls, customers):
        """Save list of customers to file."""
        try:
            with open(cls._file_path, 'w', encoding='utf-8') as f:
                json.dump([c.__dict__ for c in customers], f)
        except IOError as e:
            print(f"Error saving customers: {str(e)}")

    def delete(self):
        """Remove customer from persistent storage."""
        customers = self.load_customers()
        customers = [c for c in customers if c.email != self.email]
        self._save_all(customers)

    @classmethod
    def set_file_path(cls, new_path):
        """Set file path for testing purposes."""
        cls._file_path = new_path

    @classmethod
    def get_file_path(cls):
        """Get current file path."""
        return cls._file_path


class Reservation:
    """Handles reservation operations between customers and hotels."""
    _file_path = 'reservations.json'

    def __init__(self, customer_email, hotel_name):
        self.customer_email = customer_email
        self.hotel_name = hotel_name

    @classmethod
    def load_reservations(cls):
        """Load all reservations from JSON file."""
        try:
            if not path.exists(cls._file_path):
                return []
            with open(cls._file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading reservations: {str(e)}")
            return []

    def save(self):
        """Persist reservation to storage."""
        reservations = self.load_reservations()
        reservations.append(self.__dict__)
        try:
            with open(self._file_path, 'w', encoding='utf-8') as f:
                json.dump(reservations, f)
        except IOError as e:
            print(f"Error saving reservation: {str(e)}")

    def cancel(self):
        """Remove reservation from persistent storage."""
        reservations = self.load_reservations()
        reservations = [
            r for r in reservations
            if not (
                r['customer_email'] == self.customer_email and
                r['hotel_name'] == self.hotel_name
            )
        ]
        try:
            with open(self._file_path, 'w', encoding='utf-8') as f:
                json.dump(reservations, f)
        except IOError as e:
            print(f"Error canceling reservation: {str(e)}")

    @classmethod
    def set_file_path(cls, new_path):
        """Set file path for testing purposes."""
        cls._file_path = new_path

    @classmethod
    def get_file_path(cls):
        """Get current file path."""
        return cls._file_path


def is_valid_email(email):
    """Validate email format using regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate phone number format (10 digits)."""
    return phone.isdigit() and len(phone) == 10


def input_hotel_info():
    """Collect and validate hotel information from user."""
    name = input("Enter hotel name: ")
    while not name.strip():
        print("Name cannot be empty")
        name = input("Enter hotel name: ")

    location = input("Enter hotel location: ")
    while not location.strip():
        print("Location cannot be empty")
        location = input("Enter hotel location: ")

    while True:
        rooms = input("Enter available rooms: ")
        if rooms.isdigit():
            rooms = int(rooms)
            if rooms >= 0:
                break
        print("Invalid number of rooms")

    email = input("Enter hotel contact email: ")
    while not is_valid_email(email):
        print("Invalid email format")
        email = input("Enter hotel contact email: ")

    return name, location, rooms, email


def main_menu():
    """Display main menu and handle user input."""
    while True:
        print("\nMain Menu")
        print("1. Manage Hotels")
        print("2. Manage Customers")
        print("3. Manage Reservations")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            hotel_operations()
        elif choice == '2':
            customer_operations()
        elif choice == '3':
            reservation_operations()
        elif choice == '4':
            break
        else:
            print("Invalid choice")


def hotel_operations():
    """Handle hotel-related operations."""
    while True:
        print("\nHotel Operations")
        print("1. Create Hotel")
        print("2. Delete Hotel")
        print("3. Show Hotels")
        print("4. Modify Hotel")
        print("5. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            create_hotel()
        elif choice == '2':
            delete_hotel()
        elif choice == '3':
            display_hotels()
        elif choice == '4':
            modify_hotel()
        elif choice == '5':
            break
        else:
            print("Invalid choice")


def customer_operations():
    """Handle customer-related operations."""
    while True:
        print("\nCustomer Operations")
        print("1. Create Customer")
        print("2. Delete Customer")
        print("3. Show Customers")
        print("4. Modify Customer")
        print("5. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            create_customer()
        elif choice == '2':
            delete_customer()
        elif choice == '3':
            display_customers()
        elif choice == '4':
            modify_customer()
        elif choice == '5':
            break
        else:
            print("Invalid choice")


def reservation_operations():
    """Handle reservation-related operations."""
    while True:
        print("\nReservation Operations")
        print("1. Create Reservation")
        print("2. Cancel Reservation")
        print("3. Back")
        choice = input("Enter choice: ")
        if choice == '1':
            create_reservation()
        elif choice == '2':
            cancel_reservation()
        elif choice == '3':
            break
        else:
            print("Invalid choice")


def create_hotel():
    """Create a new hotel from user input."""
    name, location, rooms, email = input_hotel_info()
    hotel = Hotel(name, location, rooms, email)
    hotel.save()
    print("Hotel created successfully")


def delete_hotel():
    """Delete a hotel by name."""
    name = input("Enter hotel name to delete: ")
    hotels = Hotel.load_hotels()
    hotel = next((h for h in hotels if h.name == name), None)
    if hotel:
        hotel.delete()
        print("Hotel deleted successfully")
    else:
        print("Hotel not found")


def display_hotels():
    """Display all hotels."""
    hotels = Hotel.load_hotels()
    if not hotels:
        print("No hotels found")
        return
    for hotel in hotels:
        print(f"\nName: {hotel.name}")
        print(f"Location: {hotel.location}")
        print(f"Rooms Available: {hotel.rooms_available}")
        print(f"Contact Email: {hotel.email}")


def modify_hotel():
    """Modify existing hotel information."""
    name = input("Enter hotel name to modify: ")
    hotels = Hotel.load_hotels()
    hotel = next((h for h in hotels if h.name == name), None)
    if not hotel:
        print("Hotel not found")
        return

    print("\nCurrent Information:")
    print(f"1. Location: {hotel.location}")
    print(f"2. Rooms Available: {hotel.rooms_available}")
    print(f"3. Email: {hotel.email}")

    field = input("Enter field number to modify (1-3): ")
    if field == '1':
        new_value = input("Enter new location: ")
        while not new_value.strip():
            print("Location cannot be empty")
            new_value = input("Enter new location: ")
        hotel.location = new_value
    elif field == '2':
        while True:
            new_value = input("Enter new room count: ")
            if new_value.isdigit() and int(new_value) >= 0:
                hotel.rooms_available = int(new_value)
                break
            print("Invalid room count")
    elif field == '3':
        new_value = input("Enter new email: ")
        while not is_valid_email(new_value):
            print("Invalid email format")
            new_value = input("Enter new email: ")
        hotel.email = new_value
    else:
        print("Invalid field selection")
        return

    hotel.save()
    print("Hotel updated successfully")


def create_customer():
    """Create a new customer from user input."""
    name = input("Enter customer name: ")
    while not name.strip():
        print("Name cannot be empty")
        name = input("Enter customer name: ")

    email = input("Enter customer email: ")
    while not is_valid_email(email):
        print("Invalid email format")
        email = input("Enter customer email: ")

    phone = input("Enter customer phone (10 digits): ")
    while not is_valid_phone(phone):
        print("Invalid phone format")
        phone = input("Enter customer phone (10 digits): ")

    customer = Customer(name, email, phone)
    customer.save()
    print("Customer created successfully")


def delete_customer():
    """Delete a customer by email."""
    email = input("Enter customer email to delete: ")
    customers = Customer.load_customers()
    customer = next((c for c in customers if c.email == email), None)
    if customer:
        customer.delete()
        print("Customer deleted successfully")
    else:
        print("Customer not found")


def display_customers():
    """Display all customers."""
    customers = Customer.load_customers()
    if not customers:
        print("No customers found")
        return
    for customer in customers:
        print(f"\nName: {customer.name}")
        print(f"Email: {customer.email}")
        print(f"Phone: {customer.phone}")


def modify_customer():
    """Modify existing customer information."""
    email = input("Enter customer email to modify: ")
    customers = Customer.load_customers()
    customer = next((c for c in customers if c.email == email), None)
    if not customer:
        print("Customer not found")
        return

    print("\nCurrent Information:")
    print(f"1. Name: {customer.name}")
    print(f"2. Phone: {customer.phone}")

    field = input("Enter field number to modify (1-2): ")
    if field == '1':
        new_value = input("Enter new name: ")
        while not new_value.strip():
            print("Name cannot be empty")
            new_value = input("Enter new name: ")
        customer.name = new_value
    elif field == '2':
        new_value = input("Enter new phone: ")
        while not is_valid_phone(new_value):
            print("Invalid phone format")
            new_value = input("Enter new phone: ")
        customer.phone = new_value
    else:
        print("Invalid field selection")
        return

    customer.save()
    print("Customer updated successfully")


def create_reservation():
    """Create a new reservation."""
    email = input("Enter customer email: ")
    customers = Customer.load_customers()
    customer = next((c for c in customers if c.email == email), None)
    if not customer:
        print("Customer not found")
        return

    hotel_name = input("Enter hotel name: ")
    hotels = Hotel.load_hotels()
    hotel = next((h for h in hotels if h.name == hotel_name), None)
    if not hotel:
        print("Hotel not found")
        return

    if hotel.rooms_available <= 0:
        print("No available rooms in this hotel")
        return

    reservation = Reservation(email, hotel_name)
    reservation.save()
    if hotel.reserve_room():
        print("Reservation created successfully")
    else:
        print("Failed to create reservation")


def cancel_reservation():
    """Cancel an existing reservation."""
    email = input("Enter customer email: ")
    hotel_name = input("Enter hotel name: ")

    reservations = Reservation.load_reservations()
    reservation = next((r for r in reservations if r['customer_email'] == email
                       and r['hotel_name'] == hotel_name), None)
    if not reservation:
        print("Reservation not found")
        return

    Reservation(email, hotel_name).cancel()
    hotels = Hotel.load_hotels()
    hotel = next((h for h in hotels if h.name == hotel_name), None)
    if hotel:
        hotel.cancel_reservation()
    print("Reservation canceled successfully")


if __name__ == "__main__":
    main_menu()
