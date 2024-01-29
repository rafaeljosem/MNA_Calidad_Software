
'''
This module converts a list of numbers from decimal base to
hex and binary
'''

import time
import sys


def read_file(path: str) -> list:
    '''
    Reads the file where the numbers are stored
    '''
    with open(path, encoding='utf8', newline='\n') as f:
        lines = f.read().splitlines()

    if len(lines) < 1:
        raise ValueError

    lines = [float(n) for n in lines]
    return lines


def write_results(results: str) -> None:
    '''
    Writes results to a txt file
    '''
    with open('ConversionResults.txt', 'w', encoding='utf8') as f:
        f.write(results)
        f.close()


def convert_to_binary(dec_number: int, converted_num: str = '') -> str:
    '''
    Converts a list of decimal numbers to hexadecimal
    '''
    if dec_number == 0:
        return converted_num[::-1]

    converted_num += str(int(dec_number % 2))
    quotient = dec_number // 2

    return convert_to_binary(quotient, converted_num)


def convert_to_hex(dec_number: int, converted_num: str = '') -> str:
    '''
    Converts a list of decimal numbers to hexadecimal
    '''

    hex_tbl = {
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F',
    }

    if dec_number == 0:
        return converted_num[::-1]

    mod = int(dec_number % 16)
    quotient = dec_number // 16

    if mod > 9:
        mod = hex_tbl[mod]

    converted_num += str(mod)
    return convert_to_hex(quotient, converted_num)


def convert_numbers() -> None:
    '''
    Converts a list of number to hex and binary
    '''

    start_time = time.time()

    binary_nums = []
    hex_nums = []

    numbers = read_file(sys.argv[1])

    for n in numbers:
        binary_nums.append(convert_to_binary(n))
        hex_nums.append(convert_to_hex(n))

    end_time = time.time()

    elapsed_time = end_time - start_time

    results = f'''
    Decimal: {numbers}
    Binario: {binary_nums}
    Hexadecimal: {hex_nums}

    Elased time: {elapsed_time: .2f} seconds

    '''

    write_results(results)
    print(results)


try:
    if len(sys.argv) == 1:
        raise FileNotFoundError()

    convert_numbers()
except ValueError:
    print(
        'Error: el archivo debe tener al menos dos números '
        'y estos solo deben contener '
        'dígitos y punto (para el caso de los decimales). '
        '\nPor favor, revise el archivo y trate de nuevo.')
    sys.exit()
except FileNotFoundError:
    print(
        'Error: Debe proporcionar la ruta de un archivo '
        'válido que contenga números.')
