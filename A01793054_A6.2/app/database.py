'''
This module is the main database controller for
creating CRUD operations
'''

import json
import os


class Database:
    '''
    Database class to define CRUD operations
    '''

    TABLES = {
        'customers': 'customers',
        'hotels': 'hotels',
        'reservations': 'reservations'
    }

    cached_data = {
        'customers': [],
        'hotels': [],
        'reservations': []
    }

    def init(self) -> None:
        '''
        Initializes the database
        '''
        for table in self.TABLES.values():
            folder_path = 'db'
            file_path = os.path.join('db', f'{table}.json')

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            with open(file_path, mode='a', encoding='utf8'):
                pass

    def read(self, table: str) -> bool:
        '''
        Reads a table and returns the data
        '''
        file = f'db/{self.TABLES[table]}.json'
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
        try:
            with open(f'db/{self.TABLES[table]}.json',
                      encoding='utf8', mode='w') as f:
                # Check if db is loaded
                if len(self.cached_data[table]) == 0:
                    self.read(table)

                # Get next id
                next_id = self.get_next_id(table)
                entity.set_id(next_id)

                # Store the data
                data = self.to_dict(entity)
                self.cached_data[table].append(data)
                json.dump(self.cached_data[table], f)

        except TypeError:

            # Rollback
            self.cached_data[table].pop(len(self.cached_data[table]) - 1)
            entity.set_id(None)

            print(
                f'Unable to serialize the object {table} '
                f'after adding entity {entity}')
            return False

        except FileNotFoundError:

            # Rollback
            self.cached_data[table].pop(len(self.cached_data[table]) - 1)
            entity.set_id(None)

            print(f'Unable to find the database for {table}')
            return False

        return True

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

        try:
            with open(f'db/{self.TABLES[table]}.json',
                      encoding='utf8', mode='w') as f:
                json.dump(self.cached_data[table], f)

        except TypeError:
            # rollback
            self.cached_data[table].append(deleted_record)
            print(
                f'Unable to serialize the object {table} '
                f'after adding entity {entity}')
            return False

        except FileNotFoundError:
            # rollback
            self.cached_data[table].append(deleted_record)
            print(f'Unable to find the database for {table}')
            return False

        return True

    def update(self, entity: dict, table: str) -> bool:
        '''
        Updates a record
        '''
        pass

    def get_next_id(self, table: str) -> int:
        '''
        Returns the next id available in a table
        '''
        self.read(table)

        if len(self.cached_data[table]) == 0:
            return 1

        sorted_records = sorted(
            self.cached_data[table], key=lambda x: x['id'], reverse=True)

        print(sorted_records)
        return sorted_records[0]['id'] + 1

    def get_records(self, table: str) -> list:
        '''
        Get all records in a table
        '''
        if len(self.cached_data[table] == 0):
            self.init()

        return self.cached_data[table]

    def to_dict(self, entity: object) -> dict:
        '''
        Turns an object into json by
        reading its attributes
        '''
        return entity.__dict__
        # attrs = [attr for attr in dir(entity) if not attr.startswith('__')]

    def find_by(self, table: str, key: str, value: str) -> dict | None:
        '''
        Searches a hotel by name.
        If found, returns a dict, else returns None
        '''

        self.read(table)

        return next((entity for entity in self.cached_data[table]
                     if entity[key].lower() == value.lower()), None)

    def drop_table(self, table) -> bool:
        '''
        Drops a table from database
        '''

        folder_path = 'db'
        file_path = os.path.join('db', f'{table}.json')

        if not os.path.exists(folder_path):
            print(f'{file_path} does not exists')
            return False

        with open(file_path, 'w', encoding='utf8'):
            return True