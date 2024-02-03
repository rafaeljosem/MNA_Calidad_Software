'''
This program reads a pair of json files and calculates the total sales
Author: Rafael J. Mateo
Student ID: A01793054
'''

import json
import sys
import time


def read_file(path: str) -> list:
    '''
    Reads a json file
    '''
    with open(path, encoding='utf8') as f:
        data = json.load(f)
        f.close()

    return data


def read_files_in_pair() -> list:
    '''
    Reads the data in pairs
    '''

    data = []
    for i in range(0, len(sys.argv)-1, 2):

        product_list = read_file(sys.argv[i+1])
        sales = read_file(sys.argv[i + 2])
        data.append([product_list, sales])

    return data


def find_product(product_name: str, product_list: list) -> dict:
    '''
    Finds a product in the product list given a product name
    '''
    try:
        return next(iter([product for product in product_list
                          if product['title'] == product_name]))
    except StopIteration:
        return {}


def calculate_sales(product_list: list, sales: list) -> float:
    '''
    Calculates the total sales given a product_list and sales record
    '''
    total = 0
    for sale in sales:
        product = find_product(sale['Product'], product_list)

        if len(product) == 0:
            # TODO: store warnings in a dict
            print(f'Warning: product {sale['Product']}'
                  f' was not found in product list:')
            continue
        total += sale['Quantity'] * product['price']

    return total


def calculate():
    '''
    Start the total sales calculation
    '''
    start_time = time.time()
    if (len(sys.argv) - 1) % 2 != 0:
        print('Error: Debe proveer la ruta de los archivos en pares.')
        sys.exit()

    data = read_files_in_pair()

    print('\n')
    for i, (product_list, sales) in enumerate(data):
        total = calculate_sales(product_list, sales)

        print(f'Total for file# {i+1}: {total: ,.2f}')

    end_time = time.time()
    total_time = end_time - start_time

    print(f'\nTotal execution time: {total_time: .2f} seconds\n')


calculate()
