'''
Test suite for reservations
'''

import unittest
import json
import os
from app.reservation_controller import ReservationController
from app.database import Database
from app.hotel import Hotel
from app.reservation import Reservation
from app.customer import Customer
from definitions import ROOT_DIR


class TestHotelMethods (unittest.TestCase):

    '''
    Class for testing reservation controller methods
    '''

    db = None
    controller = None

    folder_path = os.path.join(ROOT_DIR, 'db')
    file_path = os.path.join(folder_path, 'reservations.json')

    def setUp(self):
        '''
        Set up the test
        '''
        self.db = Database()
        self.controller = ReservationController(db_controller=self.db)

    def test_creates_reservation(self):
        '''
        test if the create method correctly creates a new reservation
        '''

        # Arrange
        hotel = Hotel(1, 'Marriott')
        customer = Customer(1, 'John Smith')
        hotel_data = {}

        # Act
        reservation = self.controller.create_reservation(hotel, customer)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)

        # Assert
        self.assertIsInstance(reservation, Reservation)
        self.assertEqual(hotel.get_id(), 1)
        self.assertListEqual(
            hotel_data, [{
                'hotel_id': hotel.get_id(),
                'customer_id': customer.get_id(),
                'id': 1}])

    def test_deletes_reservation(self):
        '''
        Tests it deletes a reservation from db
        '''

        # 1. Arrange
        hotel = Hotel(1, 'Marriott')
        customer = Customer(1, 'John Smith')
        reservation = self.controller.create_reservation(hotel, customer)
        reservation_data = []

        # Act

        # Let's confirm that our db is not empty
        with open(self.file_path, mode='r', encoding='utf8') as f:
            reservation_data = json.load(f)
            self.assertEqual(1, len(reservation_data))

        # 2. Act
        result = self.controller.cancel_reservation(reservation)

        # 3. Assert
        self.assertTrue(result)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            reservation_data = json.load(f)
            self.assertEqual(0, len(reservation_data))

    def tearDown(self):
        '''
        Clean up database
        '''
        self.controller.drop_table()


if __name__ == '__main__':
    unittest.main()
