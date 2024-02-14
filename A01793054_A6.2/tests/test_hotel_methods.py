'''
Test suite for hotels
'''

import unittest
import json
from app.hotel_controller import HotelController
from app.database import Database
from app.hotel import Hotel


class TestHotelMethods (unittest.TestCase):

    '''
    Class for testing hotel methods
    '''

    db = None
    controller = None

    def setUp(self):
        '''
        Set up the test
        '''
        self.db = Database()
        self.controller = HotelController(db_controller=self.db)

    def test_create_hotel(self):
        '''
        test if the create method correctly creates a new hotel
        '''
        hotel_name = 'Marriot'
        hotel = self.controller.create_hotel(hotel_name)
        hotel_data = {}

        with open('db/hotels.json', mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)

        self.assertIsInstance(hotel, Hotel)
        self.assertEqual(hotel.get_id(), 1)
        self.assertListEqual(hotel_data, [{'name': hotel_name, 'id': 1}])

    def test_delete_hotel(self):
        '''
        Test the delete hotel method
        '''
        # 1. Arrange
        hotel = self.controller.create_hotel('Marriott')
        # Let's confirm that our db is not empty
        with open('db/hotels.json', mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)
            self.assertEqual(1, len(hotel_data))

        # 2. Act
        result = self.controller.delete_hotel(hotel)

        # 3. Assert
        self.assertTrue(result)

        with open('db/hotels.json', mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)
            self.assertEqual(0, len(hotel_data))

    def test_assigns_correct_id(self):
        '''
        Test if id is created correctly
        '''
        hotel_name = "Marriot"
        for i in range(3):
            hotel = self.controller.create_hotel(f'{hotel_name} {i + 1}')
            self.assertEqual(hotel.get_id(), i + 1)

    def tearDown(self):
        '''
        Clean up database
        '''
        self.controller.drop_table()


if __name__ == '__main__':
    unittest.main()
