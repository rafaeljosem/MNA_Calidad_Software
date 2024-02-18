'''
Test suite for hotels
'''

import unittest
from app.hotel import Hotel
from app.customer import Customer


class TestHotel (unittest.TestCase):

    '''
    Class for testing hotel methods
    '''

    db = None
    controller = None

    def test_sets_hotel_information(self):
        '''
        test if the create method correctly creates a new hotel
        '''
        hotel_name = 'Marriott'
        hotel_id = 1
        hotel = Hotel()

        hotel.set_id(hotel_id)
        hotel.set_name(hotel_name)

        self.assertEqual(hotel_id, hotel.get_id())
        self.assertEqual(hotel_name, hotel.get_name())

    def test_reserves_room(self):
        '''
        Test if a room is reserve correctly
        '''
        hotel_name = 'Marriott'
        hotel_id = 1
        hotel = Hotel(hotel_id=hotel_id, name=hotel_name)
        customer = Customer(1, 'John Smith')

        reservation = hotel.reserve_room(customer)

        self.assertEqual(hotel_id, reservation.get_hotel())
        self.assertEqual(1, reservation.get_customer())


if __name__ == '__main__':
    unittest.main()
