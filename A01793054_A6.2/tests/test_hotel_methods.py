'''
Test suite for hotels
'''

import unittest
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

        self.assertIsInstance(self.controller.create_hotel('Marriott'), Hotel)

    def test_delete_hotel(self):
        '''
        Test the delete hotel method
        '''
        hotel = self.controller.create_hotel('Marriott')

        self.assertTrue(self.controller.delete_hotel(hotel))

    def tearDown(self):
        '''
        Clean up database
        '''
        self.controller.drop_table()


if __name__ == '__main__':
    unittest.main()
