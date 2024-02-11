'''
Controller for hotel class
'''

from app.database import Database
from app.hotel import Hotel


class HotelController:
    '''
    Hotel Controller Class
    '''

    hotels = []
    db = None
    TABLE_NAME = 'hotels'

    def __init__(self, db_controller: Database):
        self.db = db_controller

    def create_hotel(self, hotel_name: str) -> bool | Hotel:
        '''
        Method for creating a new hotel
        '''

        if not self.find_by_name(hotel_name) is None:
            print(f'Hotel {hotel_name} already exists in database')
            return False

        hotel = Hotel(name=hotel_name)

        if self.db.create(hotel, self.TABLE_NAME):
            return hotel

        return False

    def delete_hotel(self, hotel: Hotel) -> bool:
        '''
        Deletes a hotel
        '''
        return self.db.delete(hotel, self.TABLE_NAME)

    def get_hotels(self) -> list:
        '''
        Gets all hotels in database
        '''
        return self.db.get_records('hotels')

    def to_dict(self, entity: object) -> dict:
        '''
        Turns an object into json by
        reading its attributes
        '''
        return entity.__dict__
        # attrs = [attr for attr in dir(entity) if not attr.startswith('__')]

    def find_by_name(self, name: str) -> Hotel | None:
        '''
        Searches a hotel by name.
        If found, returns a dict, else returns None
        '''

        data = self.db.find_by(self.TABLE_NAME, 'name', name)

        if data is None:
            return None

        return Hotel(hotel_id=data['id'], name=data['name'])

    def drop_table(self) -> None:
        '''
        Drops hotel table from db
        '''
        self.db.drop_table(self.TABLE_NAME)
