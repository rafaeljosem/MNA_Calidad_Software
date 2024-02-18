'''
Test suite for reservations
'''

import unittest
from app.reservation import Hotel
from app.customer import Customer
from app.reservation import Reservation


class TestReservation (unittest.TestCase):

    '''
    Class for testing reservation methods
    '''

    def test_sets_reservation_information(self):
        '''
        test if the create method correctly creates a new reservation
        '''

        hotel = Hotel(1, 'Marriott')
        customer = Customer(1, 'John Smith')
        reservation_id = 1
        reservation = Reservation()

        reservation.set_id(reservation_id)
        reservation.set_hotel(hotel)
        reservation.set_customer(customer)

        self.assertEqual(hotel.get_id(), reservation.get_hotel())
        self.assertEqual(customer.get_id(), reservation.get_customer())


if __name__ == '__main__':
    unittest.main()
