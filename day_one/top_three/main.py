from functools import reduce
from pathlib import Path
file = Path('day_one/top_three/input.txt')

def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()

def get_next_elf():
    elf = 0
    for line in get_input_data():
        if line == '':
            yield elf
            elf = 0
        else:
            elf += int(line)

def find_elf_with_most_callories():
    elf_iterator = get_next_elf()
    return reduce(which_is_more, elf_iterator, 0)

def which_is_more(first, second):
    if first > second:
        return first
    return second

if __name__ == "__main__":
    
    all_elves = sorted([x for x in get_next_elf()])
    top_three = all_elves[-3:]
    for x in top_three:
        print(str(x))
    
    print(str(sum(top_three)))