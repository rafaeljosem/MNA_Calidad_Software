'''
Reservation Class
'''

from app.hotel import Hotel
from app.customer import Customer


class Reservation:
    '''
    Reservation Class
    '''

    customer_id = None
    hotel_id = None
    id = None

    def __init__(self, reservation_id: int = None,
                 hotel: Hotel = None, customer: Customer = None):
        self.hotel_id = hotel.get_id() if hotel is not None else None
        self.customer_id = customer.get_id() if customer is not None else None
        self.id = reservation_id

    def set_hotel(self, hotel: Hotel):
        '''
        Sets the name of the hotel
        '''
        self.hotel_id = hotel.get_id()
        return self

    def get_hotel(self) -> str:
        '''
        Gets the name of the hotel
        '''
        return self.hotel_id

    def set_customer(self, customer: Customer):
        '''
        Sets the customer making the reservation
        '''
        self.customer_id = customer.get_id()
        return self

    def get_customer(self) -> str:
        '''
        Gets the name of the hotel
        '''
        return self.customer_id

    def set_id(self, reservation_id: int):
        '''
        Sets the name of the hotel
        '''
        self.id = reservation_id
        return self

    def get_id(self) -> int | None:
        '''
        Gets the name of the hotel
        '''
        return self.id
