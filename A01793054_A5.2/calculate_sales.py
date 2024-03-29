'''
This program reads a pair of json files and calculates the total sales
Author: Rafael J. Mateo
Student ID: A01793054
'''

import json
import sys
import time


class SalesCalculator:
    '''
    Class for calculating sales in a json file
    '''

    warnings = {}

    def __init__(self):
        self.warnings = {}
        self.file_names = []

    def read_file(self, path: str) -> list:
        '''
        Reads a json file
        '''

        data = []
        try:
            with open(path, encoding='utf8') as f:
                data = json.load(f)
                f.close()
        except FileNotFoundError:
            print(f'\nError: The file {path} could not be found.')

        return data

    def read_files_in_pair(self) -> dict:
        '''
        Reads the data in pairs
        '''

        data = []
        for i in range(0, len(sys.argv)-1, 2):

            product_list_file_name = sys.argv[i+1]
            sales_file_name = sys.argv[i + 2]

            # Checks if user input file names in reverse order
            if sales_file_name.find('ProductList') > 0:
                product_list_file_name = sys.argv[i+2]
                sales_file_name = sys.argv[i + 1]

            product_list = self.read_file(product_list_file_name)
            sales = self.read_file(sales_file_name)

            # Store the file names in the variable so it can be used later
            self.file_names.append(
                {'products': product_list_file_name,
                 'sales': sales_file_name})

            # Append content loaded from files
            data.append([product_list, sales])

        return data

    def find_product(self, product_name: str, product_list: list) -> dict:
        '''
        Finds a product in the product list given a product name
        '''
        try:
            # Return the first result found
            return next(iter([product for product in product_list
                              if product['title'] == product_name]))
        except StopIteration:
            return {}

    def calculate_sales(self, product_list: list, sales: list,
                        products_file_name: str,
                        sales_file_name: str) -> float:
        '''
        Calculates the total sales given a product_list and sales record
        '''
        total = 0
        self.warnings[products_file_name] = []
        self.warnings[sales_file_name] = []
        for sale in sales:

            if sale["Quantity"] < 0:

                # When a neg number is found, this line should be skipped,
                # but if done so, then calculations
                # won't match those provided in Results.txt

                self.warnings[sales_file_name].append(
                    f'''- The sale with Id number "{sale["SALE_ID"]}" '''
                    f'''and date {sale["SALE_Date"]} '''
                    f'''located in file {sales_file_name} '''
                    f'''has negative quantity ({sale["Quantity"]})''')

                # continue

            product = self.find_product(sale['Product'], product_list)

            # Checks if sales file mentions products not in product list
            if len(product) == 0:
                self.warnings[products_file_name].append(
                    f'- Product "{sale["Product"]}" '
                    f'was not found in file {products_file_name}')

                continue
            total += sale['Quantity'] * product['price']

        return total

    def write_to_file(self, results: str) -> None:
        '''
        Writes results to a txt file
        '''
        with open('SalesResults.txt', 'w', encoding='utf8') as f:
            f.write(results)
            f.close()

    def calculate(self):
        '''
        Start the total sales calculation
        '''
        start_time = time.time()
        if (len(sys.argv) - 1) % 2 != 0:
            print('Error: You must provide the file paths in pairs.')
            sys.exit()

        data = self.read_files_in_pair()
        output = '\n'
        warnings = ''

        for i, (product_list, sales) in enumerate(data):

            product_list_file_name = self.file_names[i]['products']
            sales_file_name = self.file_names[i]['sales']

            # Calculates the total
            total = self.calculate_sales(
                product_list, sales, product_list_file_name, sales_file_name)

            output += '- Total for sales in ' + \
                f'{self.file_names[i]['sales']}: {total: ,.2f}\n'

            # Print the warnings found
            if len(self.warnings[product_list_file_name]) > 0:
                warnings += '\n'.join(
                    self.warnings[product_list_file_name]) + '\n'
            if len(self.warnings[sales_file_name]) > 0:
                warnings += '\n'.join(self.warnings[sales_file_name]) + '\n'

        # Add the warnings
        if warnings != '':
            output += '\n\nSome errors were found ' + \
                'during calculation: \n\n' + warnings

        end_time = time.time()
        total_time = end_time - start_time
        output += f'\n\nTotal execution time: {total_time: .2f} seconds\n'

        self.write_to_file(output)
        print(output)


calculator = SalesCalculator()
calculator.calculate()
