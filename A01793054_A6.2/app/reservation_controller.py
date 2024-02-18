'''
Reservation Controller class
'''

from app.hotel import Hotel
from app.reservation import Reservation
from app.customer import Customer
from app.database_controller import Database


class ReservationController:
    '''
    Reservation Controller class
    '''

    reservations = []
    db = None
    TABLE_NAME = 'reservations'

    # pragma: no cover
    def __init__(self, db_controller: Database) -> bool | Reservation:
        self.db = db_controller

    def create_reservation(self, hotel: Hotel, customer: Customer):
        '''
        Creates a reservation
        '''

        reservation = Reservation(hotel=hotel, customer=customer)

        if self.db.create(reservation, self.TABLE_NAME):
            return reservation

        return False

    def cancel_reservation(self, reservation: Reservation):
        '''
        Cancels a reservation
        '''
        return self.db.delete(reservation, self.TABLE_NAME)

    # pragma: no cover
    # Drop table already tested
    def drop_table(self) -> True:
        '''
        Drops reservations table from db
        '''
        return self.db.drop_table(self.TABLE_NAME)
