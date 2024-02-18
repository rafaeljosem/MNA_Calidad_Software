'''
This module is the main database controller for
creating CRUD operations
'''

import json
import os
from definitions import ROOT_DIR


class Database:
    '''
    Database class to define CRUD operations
    '''

    TABLES = {
        'customers': 'customers',
        'hotels': 'hotels',
        'reservations': 'reservations',
        'test': 'test'
    }

    folder_path = os.path.join(ROOT_DIR, 'db')

    # Cache for fast access
    cached_data = {
        'customers': [],
        'hotels': [],
        'reservations': [],
        'test': []
    }

    def init(self) -> None:
        '''
        Initializes the database
        '''
        for table in self.TABLES.values():
            file_path = os.path.join(self.folder_path, f'{table}.json')

            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            with open(file_path, mode='a', encoding='utf8'):
                pass

    def read(self, table: str) -> bool:
        '''
        Reads a table and returns the data
        '''
        file = os.path.join(
            self.folder_path, f'{table}.json')
        try:
            if os.stat(file).st_size == 0:
                self.cached_data[table] = []
                return True

            with open(file, encoding='utf8') \
                    as f:

                data = json.load(f)
                f.close()
        except FileNotFoundError:
            self.init()
            self.cached_data[table] = []
            return True

        self.cached_data[table] = data
        return True

    def create(self, entity: object, table: str) -> bool:
        '''
        Adds new record to database
        '''

        if len(self.cached_data[table]) == 0:
            self.read(table)

        # Get next id
        next_id = self.get_next_id(table)
        entity.set_id(next_id)

        # Store the data
        data = self.to_dict(entity)
        self.cached_data[table].append(data)
        result = self.flush(table)

        if not result:
            # Rollback
            self.cached_data[table].pop(len(self.cached_data[table]) - 1)
            entity.set_id(None)
        return result

    def delete(self, entity: object, table: str) -> bool:
        '''
        Removes a record from database
        '''
        deleted_record = None

        if len(self.cached_data[table]) == 0:
            self.read(table)

        for i in range(len(self.cached_data[table])):
            record = self.cached_data[table][i]
            if record['id'] == entity.get_id():
                deleted_record = record
                del self.cached_data[table][i]
                break

        if deleted_record is None:
            print(f'Record {entity} could not be found in database')
            return False

        result = self.flush(table)

        # rollback
        if not result:
            self.cached_data[table].append(deleted_record)

        return result

    def update(self, table: str) -> bool:
        '''
        Updates a record
        '''
        return self.flush(table)

    def get_next_id(self, table: str) -> int:
        '''
        Returns the next id available in a table
        '''
        self.read(table)

        if len(self.cached_data[table]) == 0:
            return 1

        sorted_records = sorted(
            self.cached_data[table], key=lambda x: x['id'], reverse=True)

        return sorted_records[0]['id'] + 1

    def get_records(self, table: str) -> list:
        '''
        Get all records in a table
        '''
        if len(self.cached_data[self.TABLES[table]]) == 0:
            self.init()

        return self.cached_data[table]

    def to_dict(self, entity: object) -> dict:
        '''
        Turns an object into json by
        reading its attributes
        '''
        return entity.__dict__

    def find_by(self, table: str, key: str, value: str | int) -> dict | None:
        '''
        Searches a hotel by name.
        If found, returns a dict, else returns None
        '''

        self.read(table)

        return next((entity for entity in self.cached_data[table]
                     if entity[key] == value), None)

    def flush(self, table: str) -> None:
        '''
        Stores data in the database
        '''
        file_path = os.path.join(
            self.folder_path, self.TABLES[table]) + '.json'
        try:
            with open(file_path,
                      encoding='utf8', mode='w') as f:
                json.dump(self.cached_data[table], f)

        except FileNotFoundError:
            print(f'Unable to find the database for {table}')
            return False

        return True

    def drop_table(self, table) -> bool:
        '''
        Drops a table from database
        '''

        file_path = os.path.join(self.folder_path, f'{table}.json')

        if not os.path.exists(file_path):
            return False

        with open(file_path, 'w', encoding='utf8'):
            return True
