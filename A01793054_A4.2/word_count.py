'''
This program count the number of words that are stored in a file
'''
import sys
import time
import re


def read_file(path: str) -> str:
    '''
    Reads the file where the numbers are stored
    '''
    with open(path, encoding='utf8', newline='\n') as f:
        lines = re.sub(r'[^a-zA-Z0-9 ]', '', f.read().lower()).split()

    if len(lines) < 1:
        raise ValueError

    return lines


def write_results(results: str) -> None:
    '''
    Writes results to a txt file
    '''
    with open('WordCountResults.txt', 'w', encoding='utf8') as f:
        f.write(results)
        f.close()


def count_words() -> None:
    '''
    Counts the number of unique words in a text file
    '''

    start_time = time.time()
    words = read_file(sys.argv[1])
    unique_words = set(words)

    word_count = {w: words.count(w) for w in unique_words}

    end_time = time.time()

    elapsed_time = end_time - start_time

    results = (f'\nWord count: {word_count}\n\n'
               f'Elapsed time: {elapsed_time: .2f} seconds\n')

    write_results(results)
    print(results)


try:
    if len(sys.argv) == 1:
        raise FileNotFoundError()

    count_words()
except ValueError:
    print(
        'Error: Debe proporcionar una ruta válida '
        'a un archivo de texto, y este no debe estar vacío. '
        '\nPor favor, revise el archivo y trate de nuevo.')
    sys.exit()
except FileNotFoundError:
    print(
        'Error: Debe proporcionar la ruta de un archivo '
        'válido que contenga texto.')
