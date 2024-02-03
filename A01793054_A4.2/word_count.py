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
        lines = re.sub(r'[^a-zA-Z0-9 \n]', '', f.read().lower()).split()

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


def tabulate_results(data: dict) -> str:
    '''
    Format the results as a table
    '''

    output = f"{'Word':<15} {'Count':<10}\n"
    for word, count in data.items():
        output += f"{word:<15} {count:<10}\n"
    return output


def count_words() -> None:
    '''
    Counts the number of unique words in a text file
    '''

    start_time = time.time()
    output = ''

    for i in range(1, len(sys.argv)):

        words = read_file(sys.argv[i])
        unique_words = set(words)

        word_count = {w: words.count(w) for w in unique_words}
        word_count_sorted = dict(sorted(word_count.items(),
                                        key=lambda word: word[1],
                                        reverse=True))
        output += f'\n========== Results for {sys.argv[i]} ==========\n\n' + \
            tabulate_results(word_count_sorted)

    end_time = time.time()
    elapsed_time = end_time - start_time

    output += f'\nElapsed time: {elapsed_time: .2f} seconds\n'

    print(output)
    write_results(output)

    # write_results(results)
    # print(results)


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
