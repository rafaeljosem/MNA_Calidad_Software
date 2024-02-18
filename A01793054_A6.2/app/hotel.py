'''
Hotel class
'''

from app.customer import Customer


class Hotel:
    '''
    Hotel class
    '''

    name = ''
    id = None
    reservations = []

    def __init__(self, hotel_id: int = None, name: str = ''):
        self.name = name
        self.id = hotel_id

    def set_name(self, name: str):
        '''
        Sets the name of the hotel
        '''
        self.name = name
        return self

    def get_name(self) -> str:
        '''
        Gets the name of the hotel
        '''
        return self.name

    def set_id(self, hotel_id: int):
        '''
        Sets the name of the hotel
        '''
        self.id = hotel_id
        return self

    def get_id(self) -> int | None:
        '''
        Gets the name of the hotel
        '''
        return self.id

    def reserve_room(self, customer: Customer):
        '''
        Reserves a room
        '''
        # pylint: disable=import-outside-toplevel
        from app.reservation import Reservation
        reservation = Reservation(hotel=self, customer=customer)
        self.reservations.append(reservation)
        return reservation
