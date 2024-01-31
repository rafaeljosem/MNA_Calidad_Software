
'''
This module converts a list of numbers from decimal base to
hex and binary
'''

import time
import sys
import re


def read_file(path: str) -> list:
    '''
    Reads the file where the numbers are stored
    '''
    with open(path, encoding='utf8', newline='\n') as f:
        lines = re.sub(r'[^-0-9A-Za-z.\-\n]', ' ', f.read()).split()

    if len(lines) < 1:
        raise ValueError

    lines = [int(n) for n in lines if is_number(n)]
    return lines


def is_number(s: str) -> bool:
    '''
    Checks if a string is a number
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False


def write_results(results: str) -> None:
    '''
    Writes results to a txt file
    '''
    with open('ConversionResults.txt', 'w', encoding='utf8') as f:
        f.write(results)
        f.close()


def convert_to_binary(dec_number: int, converted_num: str = '',
                      num_bits: int = 10) -> str:
    '''
    Converts a list of decimal numbers to hexadecimal
    '''
    if dec_number == 0:
        if converted_num == '':
            return '0'.zfill(num_bits)

        return converted_num[::-1].zfill(num_bits)

    remainder = dec_number % 2
    converted_num += str(remainder)

    # 2's complement for handling negative numbers
    if dec_number < 0:
        dec_number = (dec_number + (1 << num_bits)) // 2

    quotient = dec_number // 2

    return convert_to_binary(quotient, converted_num, num_bits)


def convert_to_hex(dec_number: int,
                   num_bits: int = 32, leading_zero=True) -> str:
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

    # 2's complement for handling negative numbers
    if dec_number < 0:
        dec_number = (1 << num_bits) + dec_number

    if dec_number == 0:
        return '0' if leading_zero else ''

    remainder = dec_number % 16
    hex_char = str(remainder) if remainder < 10 else hex_tbl[remainder]

    quotient = dec_number // 16
    return convert_to_hex(quotient, num_bits, False) + hex_char


def tabulate_results(columns: list, data: list) -> str:
    '''
    Format the results into a table
    '''
    # Transpose the data
    data = list(zip(*data))

    table = ''

    line = "+" + "+".join(["-" * 36 for _ in columns]) + "+"
    header_line = "+" + "+".join(["=" * 36 for _ in columns]) + "+"

    table += header_line + '\n'
    table += " " + "|".join(f"{col:^36}" for col in columns) + "|\n"

    table += line + '\n'

    for i, item in enumerate(data):
        row_data = item if i < len(
            data) else ["" for _ in range(len(columns))]

        row = "|".join(f"{value:^36}" for value in row_data) + '|\n'
        table += ' ' + row + line + "\n"

    return table


def convert_numbers() -> None:
    '''
    Converts a list of number to hex and binary
    '''

    start_time = time.time()
    columns = ['Decimal', 'Binary', 'Hex']
    output = ''

    for i in range(1, len(sys.argv)):

        binary_nums = []
        hex_nums = []

        numbers = read_file(sys.argv[i])

        for n in numbers:

            binary_nums.append(convert_to_binary(n))
            hex_nums.append(convert_to_hex(n))

        output += f'Results for {sys.argv[i]}\n' + tabulate_results(
            columns, [numbers, binary_nums, hex_nums]) + '\n\n'

    end_time = time.time()

    elapsed_time = end_time - start_time

    output += f'Elased time: {elapsed_time: .2f} seconds'

    write_results(output)
    print(output)


try:
    if len(sys.argv) == 1:
        raise FileNotFoundError()

    convert_numbers()
except ValueError as e:
    print(
        e)
    sys.exit()
except FileNotFoundError:
    print(
        'Error: Debe proporcionar la ruta de un archivo '
        'válido que contenga números.')
