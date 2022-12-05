from functools import reduce
from pathlib import Path

def get_input_data(file: Path):
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()

def get_next_elf(file:Path):
    elf = 0
    for line in get_input_data(file):
        if line == '':
            yield elf
            elf = 0
        else:
            elf += int(line)

def find_elf_with_most_callories(file):
    elf_iterator = get_next_elf(file)
    return reduce(which_is_more, elf_iterator, 0)

def which_is_more(first, second):
    if first > second:
        return first
    return second

if __name__ == "__main__":
    file = Path('day_one/elf_calories/input.txt')
    print(find_elf_with_most_callories(file))