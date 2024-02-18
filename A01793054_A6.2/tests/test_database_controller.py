'''
Test suite for database
'''

import unittest
import json
import os
from app.database import Database
from definitions import ROOT_DIR
from tests.dummy import Dummy


def file_exists(directory, filename):
    '''
    Method for asserting if a file exists
    '''
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


class TestDatabaseController (unittest.TestCase):

    '''
    Class for testing database methods
    '''

    db = None
    controller = None
    dummy = None
    db_tbl_name = 'test'

    folder_path = os.path.join(ROOT_DIR, 'db')
    file_path = os.path.join(folder_path, 'test.json')

    def setUp(self):
        '''
        Set up the test
        '''
        self.db = Database()
        self.dummy = Dummy(name='dummy test', num=123)

    def test_persists_data(self):
        '''
        test if the create method correctly creates a new database
        '''
        # 1. Arrange
        database_data = {}

        # 2. Act
        self.db.create(self.dummy, self.db_tbl_name)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            database_data = json.load(f)

        # 3. Assert
        self.assertListEqual(
            database_data, [{
                'name': self.dummy.get_name(),
                'id': 1,
                'num': self.dummy.get_num()}])

    def test_deletes_data(self):
        '''
        Test the delete database method
        '''
        # 1. Arrange
        self.db.create(self.dummy, self.db_tbl_name)
        # Let's confirm that our db is not empty
        with open(self.file_path, mode='r', encoding='utf8') as f:
            database_data = json.load(f)
            self.assertEqual(1, len(database_data))

        # 2. Act
        result = self.db.delete(self.dummy, self.db_tbl_name)

        # 3. Assert
        self.assertTrue(result)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            database_data = json.load(f)
            self.assertEqual(0, len(database_data))

    def test_assigns_correct_id(self):
        '''
        Test if id is created correctly
        '''
        for i in range(3):
            dummy = Dummy(num=i, name=f'dummy {i}')
            self.db.create(dummy, self.db_tbl_name)
            self.assertEqual(dummy.get_id(), i + 1)

    def test_it_updates_data(self):
        '''
        Test if modified database info is stored to db
        '''
        # 1. Arrange
        new_name = 'Dummy name changed'
        self.db.create(self.dummy, self.db_tbl_name)
        self.dummy.set_name(new_name)

        # 2. Act
        result = self.db.update(self.db_tbl_name)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            dummy_data = json.load(f)

        # 3. Assert

        self.assertTrue(result)
        self.assertEqual(new_name, dummy_data[0]['name'])

    def test_it_finds_data(self):
        '''
        Tests it finds a database by id
        '''
        # 1. Arrange
        dummy_name = "Test"
        dummies = []
        for i in range(3):
            dummy_name = dummy_name + f' {i + 1}'
            dummy = Dummy(name=dummy_name, num=i)
            self.db.create(dummy, self.db_tbl_name)
            dummies.append(dummy)

        # 2. Act and Assert

        for i, dummy in enumerate(dummies):
            data = self.db.find_by(self.db_tbl_name, 'id', i + 1)
            self.assertEqual(data['id'], dummy.get_id())
            self.assertEqual(data['name'], dummy.get_name())

    def test_it_creates_file_if_not_exists(self):
        '''
        Test if file is created if it doesn't exist
        '''
        # 1. Arrange
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
        except OSError as e:
            print(f"Failed with: {e.strerror}")
        # 2. Act
        self.db.create(self.dummy, self.db_tbl_name)

        # 3 Assert
        self.assertTrue(file_exists(self.folder_path, 'test.json'))

    def test_it_drops_table(self):
        '''
        Test if it drops the database table from db
        '''

        # 1. Arrange
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        with open(self.file_path, mode='a', encoding='utf8') as f:
            f.write('{}')

        # 2. Act
        result = self.db.drop_table(self.db_tbl_name)

        # 3. Assert
        self.assertTrue(os.stat(self.file_path).st_size == 0)
        self.assertTrue(result)

    def test_it_does_not_drop_table(self):
        '''
        Test it returns false if a dir does not exist
        '''
        # 1. Arrange

        if os.path.exists(self.folder_path):
            try:
                os.remove(self.file_path)
            except OSError as e:
                print(f"Failed with: {e.strerror}")

        # 2. Act
        result = self.db.drop_table(self.db_tbl_name)

        # 3. Assert
        self.assertFalse(result)

    def test_it_gets_records(self):
        '''
        Test it gets all cached records
        '''

        self.db.create(self.dummy, self.db_tbl_name)

        records = self.db.get_records(self.db_tbl_name)

        self.assertEqual(1, len(records))

    def tearDown(self):
        '''
        Clean up database
        '''
        self.db.drop_table(self.db_tbl_name)


if __name__ == '__main__':
    unittest.main()
