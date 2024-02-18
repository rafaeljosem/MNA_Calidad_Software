'''
Test suite for hotels
'''

import unittest
import json
import os
from app.hotel_controller import HotelController
from app.database_controller import Database
from app.hotel import Hotel
from definitions import ROOT_DIR


def file_exists(directory, filename):
    '''
    Method for asserting if a file exists
    '''
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


class TestHotelController (unittest.TestCase):

    '''
    Class for testing hotel methods
    '''

    db = None
    controller = None

    folder_path = os.path.join(ROOT_DIR, 'db')
    file_path = os.path.join(folder_path, 'hotels.json')

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

        with open(self.file_path, mode='r', encoding='utf8') as f:
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
        with open(self.file_path, mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)
            self.assertEqual(1, len(hotel_data))

        # 2. Act
        result = self.controller.delete_hotel(hotel)

        # 3. Assert
        self.assertTrue(result)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)
            self.assertEqual(0, len(hotel_data))

    def test_it_modifies_a_hotel(self):
        '''
        Test if modified hotel info is stored to db
        '''
        # 1. Arrange

        hotel_name = 'Marriot'
        new_name = 'Hilton'
        hotel = self.controller.create_hotel(hotel_name)
        hotel.set_name(new_name)

        # 2. Act
        result = self.controller.update_hotel()

        with open(self.file_path, mode='r', encoding='utf8') as f:
            hotel_data = json.load(f)

        # 3. Assert

        self.assertTrue(result)
        self.assertEqual(new_name, hotel_data[0]['name'])

    def test_it_displays_hotel_info_correctly(self):
        '''
        Test if hotel info is displayed correctly
        '''
        # Arrange
        hotel = Hotel(1, 'Marriott')

        expected = f'\nHotel Id: {hotel.get_id()}' \
            f'\nHotel Name: {hotel.get_name()}'

        # Act
        result = self.controller.display_hotel_info(hotel)

        # Assert
        self.assertEqual(expected, result)

    def test_it_finds_hotel_by_name(self):
        '''
        Tests it finds a hotel by id
        '''
        # 1. Arrange
        hotel_base_name = "Marriot"
        hotels = []
        for i in range(3):
            hotel_name = hotel_base_name + f' {i + 1}'
            self.controller.create_hotel(hotel_name)
            hotels.append({'id': i+1, 'name': hotel_name})

        # 2. Act and Assert

        for i, data in enumerate(hotels):
            hotel = self.controller.find_by_name(data['name'])
            self.assertEqual(data['id'], hotel.get_id())
            self.assertEqual(data['name'], hotel.get_name())

    def tearDown(self):
        '''
        Clean up database
        '''
        self.controller.drop_table()


if __name__ == '__main__':
    unittest.main()
