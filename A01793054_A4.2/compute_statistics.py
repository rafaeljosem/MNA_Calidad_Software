'''
This module calculates the mean from numbers stored
in a file
'''

import sys
import time
import re


def read_file(path: str) -> dict:
    '''
    Reads the file where the numbers are stored
    '''
    with open(path, encoding='utf8', newline='\n') as f:
        lines = re.sub(r'[^0-9A-Za-z.\n]', ' ', f.read()).split()

    if len(lines) < 2:
        raise ValueError

    valid_lines = [float(n) for n in lines if is_number(n)]
    return {
        'original': lines,
        'valid': valid_lines
    }


def calculate_mean(numbers: list) -> float:
    '''
    Calculates the mean from a list of numbers.
    If a character that is not a number is detected,
    then it's skipped from the calculation
    '''
    size = len(numbers)
    total = 0

    for n in numbers:
        total += float(n)

    return total/size


def is_number(s: str) -> bool:
    '''
    Checks if a string is a number
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False


def calculate_median(numbers: list) -> float:
    '''
    Calculates the median from a list of numbers
    '''
    size = len(numbers)
    numbers.sort()

    if size % 2 == 0:
        pos1 = int((size/2)) - 1
        pos2 = pos1 + 1

        return (numbers[pos1] + numbers[pos2])/2

    pos = ((size // 2) + (size % 2 > 0)) - 1

    if pos < 0:
        return numbers[0]

    return numbers[pos]


def calculate_variance(numbers: list) -> float:
    '''
    Calculates the variance given a list of number.
    This method assumes that the numbers come from a
    population and not a sample.
    '''
    size = len(numbers)
    total = 0
    mean = calculate_mean(numbers)

    for n in numbers:
        total += (n - mean)**2

    return total/size


def calculate_mode(numbers: list) -> list | None:
    '''
    Calcualtes the mode from a list of numbers
    '''
    count = {n: numbers.count(n) for n in set(numbers)}
    max_count = max(count.values())

    if max_count == 1:
        return None

    mode = [n for n in count if count[n] == max_count]

    return mode


def write_results(results: str) -> None:
    '''
    Writes results to a txt file
    '''
    with open('StatisticsResults.txt', 'w', encoding='utf8') as f:
        f.write(results)
        f.close()


def tabulate_results(columns: str, row_labels: str, data: list) -> str:
    '''
    Format the results into a table
    '''
    # Transpose the data
    data = list(zip(*data))

    table = '\nStatistics Result\n'

    line = "+" + "+".join(["-" * 15 for _ in columns]) + "+"
    header_line = "+" + "+".join(["=" * 15 for _ in columns]) + "+"

    table += header_line + '\n'
    table += f"|{'':<18}" + "|".join(f"{col:^12}" for col in columns) + "|\n"

    table += line + '\n'

    for i, label in enumerate(row_labels):
        row_data = data[i] if i < len(
            data) else ["" for _ in range(len(columns))]

        row = f"|{label:<18}" + \
            "|".join(f"{value:^12}" for value in row_data) + '|\n'
        table += row + line + "\n"

    return table


def calculate_statistics():
    '''
    Call helper functions to calculate the statistics
    and then print the results on screen
    '''
    start_time = time.time()

    results = []

    for i in range(1, len(sys.argv)):

        numbers = read_file(sys.argv[i])

        mean = calculate_mean(numbers['valid'])
        median = calculate_median(numbers['valid'])
        mode = calculate_mode(numbers['valid'])
        variance = calculate_variance(numbers['valid'])
        stddev = variance**0.5

        results.append([
            len(numbers['original']),
            len(numbers['valid']),
            f'{mean:.5}',
            f'{median:.5}',
            ', '.join(map(str, mode)) if mode is not None else 'N/A',
            f'{variance:.5}',
            f'{stddev:.5}',])

    end_time = time.time()
    elapsed_time = end_time - start_time

    column_names = sys.argv[1:]
    row_names = ['Total', 'Valid', 'Mean',
                 'Median', 'Mode', 'Variance', 'Std. Dev.']

    output = (tabulate_results(column_names, row_names, results) +
              '\n' + f'Total time: {elapsed_time: .2f} seconds')

    print(output)
    write_results(output)


try:

    if len(sys.argv) == 1:
        raise FileNotFoundError()

    calculate_statistics()
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
