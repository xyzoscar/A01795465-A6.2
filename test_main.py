"""
Unit tests for the Hotel Reservation System.
Covers core classes, validation functions, and menu operations.
"""
import unittest
from unittest.mock import patch
import os

from main import (
    Hotel,
    Customer,
    Reservation,
    is_valid_email,
    is_valid_phone,
    main_menu,
    hotel_operations,
    customer_operations,
    reservation_operations,
    create_hotel,
    delete_hotel,
    display_hotels,
    modify_hotel,
    create_customer,
    delete_customer,
    display_customers,
    modify_customer,
    create_reservation,
    cancel_reservation
)


class TestMainMenu(unittest.TestCase):
    """
    Tests for main menu functionality.
    """
    @patch('builtins.input', side_effect=['4'])
    def test_main_menu_exit(self, _mock_input):
        """
        Tests the main menu exit functionality.
        """
        main_menu()

    @patch('builtins.input', side_effect=['9', '4'])
    def test_main_menu_invalid_choice_then_exit(self, _mock_input):
        """
        Tests the main menu function by simulating an
        invalid choice followed by an exit.
        """
        main_menu()


class TestHotelMenuOperations(unittest.TestCase):
    """
    Tests for hotel menu operations.
    """
    @patch('builtins.input', side_effect=['5'])
    def test_hotel_operations_back(self, _mock_input):
        """Tests returning to the previous menu from hotel operations."""
        hotel_operations()

    @patch('builtins.input', side_effect=['9', '5'])
    def test_hotel_operations_invalid_choice(self, _mock_input):
        """Tests handling of an invalid menu choice in hotel operations."""
        hotel_operations()


class TestCustomerMenuOperations(unittest.TestCase):
    """
    Tests for customer menu operations, validating
    input handling and navigation.
    """

    @patch('builtins.input', side_effect=['5'])
    def test_customer_operations_back(self, _mock_input):
        """Tests returning to the previous menu from customer operations."""
        customer_operations()

    @patch('builtins.input', side_effect=['9', '5'])
    def test_customer_operations_invalid_choice(self, _mock_input):
        """Tests handling of an invalid menu choice in customer operations."""
        customer_operations()


class TestReservationMenuOperations(unittest.TestCase):
    """
    Tests for reservation menu operations, ensuring
    correct input handling and navigation.
    """
    @patch('builtins.input', side_effect=['3'])
    def test_reservation_operations_back(self, _mock_input):
        """Tests returning to the previous menu from reservation operations."""
        reservation_operations()

    @patch('builtins.input', side_effect=['9', '3'])
    def test_reservation_operations_invalid_choice(self, _mock_input):
        """
        Tests handling of an invalid menu
        choice in reservation operations.
        """
        reservation_operations()


class TestHotel(unittest.TestCase):
    """
    Test suite for the Hotel class, ensuring correct creation,
    saving, and loading of hotel data
    """
    def setUp(self):
        Hotel.set_file_path('test_hotels.json')
        if os.path.exists(Hotel.get_file_path()):
            os.remove(Hotel.get_file_path())

    def test_create_and_save_hotel(self):
        """
        Tests the creation and persistence of a Hotel object,
        verifying correct data storage and retrieval.
        """
        hotel = Hotel("Awesome Hotel", "Paris", 50, "info@examplehotel.com")
        hotel.save()
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0].name, "Awesome Hotel")

    def test_delete_hotel(self):
        """
        Tests the deletion of a hotel instance and verifies that
        the hotel list is empty after deletion.
        """
        hotel = Hotel("Awesome Hotel", "Paris", 50, "info@examplehotel.com")
        hotel.save()
        hotel.delete()
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 0)

    def test_reserve_room(self):
        """
        Tests the room reservation functionality of the Hotel class.
        """
        hotel = Hotel("Awesome Hotel", "Paris", 1, "info@examplehotel.com")
        hotel.save()
        self.assertTrue(hotel.reserve_room())
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].rooms_available, 0)
        self.assertFalse(hotel.reserve_room())

    def test_cancel_reservation(self):
        """
        Tests the cancellation of a reservation and
        verifies that the number of available rooms is updated correctly.
        """
        hotel = Hotel("Awesome Hotel", "Paris", 0, "info@examplehotel.com")
        hotel.save()
        hotel.cancel_reservation()
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].rooms_available, 1)

    def test_load_hotels_invalid_file(self):
        """
        Tests loading hotels from an invalid JSON file.
        """
        with open(Hotel.get_file_path(), 'w', encoding='utf-8') as f:
            f.write("invalid json")
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 0)


class TestCustomer(unittest.TestCase):
    """
    Tests for the Customer class.
    """
    def setUp(self):
        Customer.set_file_path('test_customers.json')
        if os.path.exists(Customer.get_file_path()):
            os.remove(Customer.get_file_path())

    def test_create_and_save_customer(self):
        """
        Tests the creation and saving of a customer,
        and verifies that the customer
        is correctly saved and loaded with the expected email.
        """
        customer = Customer("Arthur", "email@example.com", "1234567890")
        customer.save()
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].email, "email@example.com")

    def test_delete_customer(self):
        """
        Tests the deletion of a customer and verifies
        that the customer list is empty.
        """
        customer = Customer("Arthur", "email@example.com", "1234567890")
        customer.save()
        customer.delete()
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 0)


class TestReservation(unittest.TestCase):
    """
    Unit tests for the Reservation class, including
    creation and cancellation of reservations.
    """
    def setUp(self):
        Hotel.set_file_path('test_hotels.json')
        Customer.set_file_path('test_customers.json')
        Reservation.set_file_path('test_reservations.json')
        for fp in [
            Hotel.get_file_path(),
            Customer.get_file_path(),
            Reservation.get_file_path()
        ]:
            if os.path.exists(fp):
                os.remove(fp)

    def test_create_and_cancel_reservation(self):
        """
        Tests the creation and cancellation of a hotel reservation.
        """
        hotel = Hotel("Awesome Hotel", "Paris", 5, "info@example.com")
        hotel.save()
        customer = Customer("Arthur", "email@example.com", "1234567890")
        customer.save()

        reservation = Reservation("email@example.com", "Awesome Hotel")
        reservation.save()

        hotels = Hotel.load_hotels()
        hotel = hotels[0]
        self.assertTrue(hotel.reserve_room())

        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(
            reservations[0]["customer_email"],
            "email@example.com"
        )
        self.assertEqual(reservations[0]["hotel_name"], "Awesome Hotel")

        reservation.cancel()
        hotels = Hotel.load_hotels()
        hotel = hotels[0]
        hotel.cancel_reservation()

        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 0)
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].rooms_available, 5)


class TestValidationFunctions(unittest.TestCase):
    """
    Unit tests for validation functions: is_valid_email and is_valid_phone.
    """
    def test_is_valid_email(self):
        """
        Tests the is_valid_email function with various email formats.
        """
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertTrue(is_valid_email("user.name@domain.co"))
        self.assertFalse(is_valid_email("invalid.email"))
        self.assertFalse(is_valid_email("user@.com"))

    def test_is_valid_phone(self):
        """
        Tests the is_valid_phone function.

        Valid: "1234567890"
        Invalid (short): "1234"
        Invalid (non-numeric): "abcdefghij"
        """
        self.assertTrue(is_valid_phone("1234567890"))
        self.assertFalse(is_valid_phone("1234"))
        self.assertFalse(is_valid_phone("abcdefghij"))


class TestHotelOperations(unittest.TestCase):
    """
    Unit tests for hotel operations including creation,
    deletion, and display of hotels.
    """
    def setUp(self):
        Hotel.set_file_path('test_hotels.json')
        if os.path.exists(Hotel.get_file_path()):
            os.remove(Hotel.get_file_path())

    @patch('builtins.input', side_effect=[
        'Test Hotel',
        'Test Location',
        '10',
        'test@example.com'
    ])
    def test_create_hotel_op(self, _mock_input):
        """
        Tests the creation of a hotel and verifies that it
        is correctly added to the list of hotels.
        """
        create_hotel()
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0].name, "Test Hotel")

    @patch('builtins.input', side_effect=['NonExistent Hotel'])
    def test_delete_nonexistent_hotel_op(self, _mock_input):
        """
        Tests the deletion of a nonexistent hotel and verifies
        that the hotel list remains empty.
        """
        delete_hotel()
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 0)

    @patch('builtins.print')
    def test_display_hotels_no_hotels(self, mock_print):
        """
        Test case for display_hotels function when no hotels are found.
        """
        display_hotels()
        mock_print.assert_any_call("No hotels found")

    @patch('builtins.print')
    def test_display_hotels_with_hotels(self, mock_print):
        """
        Tests that the display_hotels function correctly
        prints the details of saved hotels.
        """
        Hotel("Hotel1", "Location1", 10, "contact1@example.com").save()
        Hotel("Hotel2", "Location2", 5,  "contact2@example.com").save()
        display_hotels()
        printed_calls = [args[0] for args, _ in mock_print.call_args_list]
        self.assertTrue(any("Hotel1" in line for line in printed_calls))
        self.assertTrue(any("Hotel2" in line for line in printed_calls))


class TestModifyHotelScenarios(unittest.TestCase):
    """
    Tests for hotel modification scenarios.
    """
    def setUp(self):
        Hotel.set_file_path('test_hotels.json')
        if os.path.exists(Hotel.get_file_path()):
            os.remove(Hotel.get_file_path())
        Hotel("Sample Hotel", "Sample City", 5, "hotel@example.com").save()

    @patch('builtins.input', side_effect=['BadHotel'])
    def test_modify_hotel_not_found(self, _mock_input):
        """
        Test case for modifying a hotel that is not found.
        """
        modify_hotel()
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].name, "Sample Hotel")

    @patch('builtins.input', side_effect=['Sample Hotel', '4'])
    def test_modify_hotel_invalid_field(self, _mock_input):
        """
        Tests the modify_hotel function to ensure that an
        invalid field does not alter the hotel's email.
        """
        modify_hotel()
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].email, "hotel@example.com")


class TestCustomerOperations(unittest.TestCase):
    """
    Unit tests for customer operations including
    creation, display, deletion, and modification.
    """
    def setUp(self):
        Customer.set_file_path('test_customers.json')
        if os.path.exists(Customer.get_file_path()):
            os.remove(Customer.get_file_path())

    @patch('builtins.input', side_effect=[
        'Arthur',
        'email@example.com',
        '1234567890'
    ])
    def test_create_customer_op(self, _mock_input):
        """
        Tests the creation of a customer and verifies
        that the customer is correctly added to the list
        of customers.
        """
        create_customer()
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].name, "Arthur")

    @patch('builtins.print')
    def test_display_customers_no_customers(self, mock_print):
        """
        Test display_customers function when there are no customers.
        """
        display_customers()
        mock_print.assert_any_call("No customers found")

    @patch('builtins.input', side_effect=['email@example.com'])
    def test_delete_customer_op(self, _mock_input):
        """
        Tests the delete_customer function by creating a customer,
        saving it, deleting it, and then verifying that the
        customer list is empty.
        """
        c = Customer("Arthur", "email@example.com", "1234567890")
        c.save()
        delete_customer()
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 0)

    @patch('builtins.input', side_effect=[
        'email@example.com',
        '1',
        'New Name'
    ])
    def test_modify_customer_op(self, _mock_input):
        """
        Test the modify_customer function to ensure
        it updates a customer's name correctly.
        """
        c = Customer("Arthur", "email@example.com", "1234567890")
        c.save()

        modify_customer()

        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].name, "New Name")


class TestReservationOperations(unittest.TestCase):
    """
    Unit tests for reservation operations including
    creation and cancellation.
    """
    def setUp(self):
        Hotel.set_file_path('test_hotels.json')
        Customer.set_file_path('test_customers.json')
        Reservation.set_file_path('test_reservations.json')
        for fp in [
            Hotel.get_file_path(),
            Customer.get_file_path(),
            Reservation.get_file_path()
        ]:
            if os.path.exists(fp):
                os.remove(fp)

    @patch('builtins.input', side_effect=[
        'email@example.com',
        'Awesome Hotel']
    )
    def test_create_reservation_customer_not_found(self, _mock_input):
        """
        Tests that creating a reservation fails
        when the customer is not found.
        """
        create_reservation()
        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 0)

    @patch('builtins.input', side_effect=['email@example.com', 'FullHotel'])
    def test_create_reservation_no_rooms(self, _mock_input):
        """
        Test that creating a reservation fails when there
        are no available rooms.
        """
        Customer("Arthur", "email@example.com", "1234567890").save()
        Hotel("FullHotel", "SomeCity", 0, "test@fullhotel.com").save()
        create_reservation()
        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 0)

    @patch('builtins.input', side_effect=[
        'email@example.com',
        'TestHotel'
    ])
    def test_cancel_reservation_op(self, _mock_input):
        """
        Tests the cancellation of a reservation and
        verifies that the reservation is removed and
        the room is made available again.
        """
        h = Hotel("TestHotel", "TestCity", 1, "test@hotel.com")
        h.save()

        c = Customer("Arthur", "email@example.com", "1234567890")
        c.save()

        r = Reservation("email@example.com", "TestHotel")
        r.save()
        h.reserve_room()

        cancel_reservation()

        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 0)

        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0].rooms_available, 1)


if __name__ == '__main__':
    unittest.main()
