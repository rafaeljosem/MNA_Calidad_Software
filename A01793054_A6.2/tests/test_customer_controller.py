'''
Test suite for customers
'''

import unittest
import json
import os
from app.customer_controller import CustomerController
from app.database_controller import Database
from app.customer import Customer
from definitions import ROOT_DIR


def file_exists(directory, filename):
    '''
    Method for asserting if a file exists
    '''
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


class TestCustomerController (unittest.TestCase):

    '''
    Class for testing customer methods
    '''

    db = None
    controller = None

    folder_path = os.path.join(ROOT_DIR, 'db')
    file_path = os.path.join(folder_path, 'customers.json')

    def setUp(self):
        '''
        Set up the test
        '''
        self.db = Database()
        self.controller = CustomerController(db_controller=self.db)

    def test_create_customer(self):
        '''
        test if the create method correctly creates a new customer
        '''
        customer_name = 'John Smith'
        customer = self.controller.create_customer(customer_name)
        customer_data = {}

        with open(self.file_path, mode='r', encoding='utf8') as f:
            customer_data = json.load(f)

        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.get_id(), 1)
        self.assertListEqual(customer_data, [{'name': customer_name, 'id': 1}])

    def test_delete_customer(self):
        '''
        Test the delete customer method
        '''
        # 1. Arrange
        customer = self.controller.create_customer('John Smith')
        # Let's confirm that our db is not empty
        with open(self.file_path, mode='r', encoding='utf8') as f:
            customer_data = json.load(f)
            self.assertEqual(1, len(customer_data))

        # 2. Act
        result = self.controller.delete_customer(customer)

        # 3. Assert
        self.assertTrue(result)

        with open(self.file_path, mode='r', encoding='utf8') as f:
            customer_data = json.load(f)
            self.assertEqual(0, len(customer_data))

    def test_it_modifies_a_customer(self):
        '''
        Test if modified customer info is stored to db
        '''
        # 1. Arrange

        customer_name = 'Marriot'
        new_name = 'Hilton'
        customer = self.controller.create_customer(customer_name)
        customer.set_name(new_name)

        # 2. Act
        result = self.controller.update_customer()

        with open('db/customers.json', mode='r', encoding='utf8') as f:
            customer_data = json.load(f)

        # 3. Assert

        self.assertTrue(result)
        self.assertEqual(new_name, customer_data[0]['name'])

    def test_it_displays_customer_info_correctly(self):
        '''
        Test if customer info is displayed correctly
        '''
        # Arrange
        customer = Customer(1, 'Marriott')

        expected = f'\nCustomer Id: {customer.get_id()}' \
            f'\nCustomer Name: {customer.get_name()}'

        # Act
        result = self.controller.display_customer_info(customer)

        # Assert
        self.assertEqual(expected, result)

    def tearDown(self):
        '''
        Clean up database
        '''
        self.controller.drop_table()


if __name__ == '__main__':
    unittest.main()
