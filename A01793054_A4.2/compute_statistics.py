'''
This module calculates the mean from numbers stored
in a file
'''

import sys
import time


def read_file(path: str) -> list:
    '''
    Reads the file where the numbers are stored
    '''
    with open(path, encoding='utf8', newline='\n') as f:
        lines = f.read().splitlines()

    if len(lines) < 2:
        raise ValueError

    lines = [float(n) for n in lines]
    return lines


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


def calculate_mode(numbers: list) -> float:
    '''
    Calcualtes the mode from a list of numbers
    '''
    count = {n: numbers.count(n) for n in set(numbers)}
    max_count = max(count.values())

    mode = [n for n in count if count[n] == max_count]

    return mode


def write_results(results: str) -> None:
    '''
    Writes results to a txt file
    '''
    with open('StatisticsResults.txt', 'w', encoding='utf8') as f:
        f.write(results)
        f.close()


def calculate_statistics():
    '''
    Call helper functions to calculate the statistics
    and then print the results on screen
    '''

    numbers = read_file(sys.argv[1])

    start_time = time.time()

    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_variance(numbers)

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = f'''
    Mean: {mean}
    Median: {median}
    Mode: {mode}
    Variance: {variance}
    Std. Dev (population): {variance**0.5}

    Total time: {elapsed_time: .2f} seconds
   '''
    write_results(results)
    print(results)


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
