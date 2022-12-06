from functools import reduce
from pathlib import Path
from typing import Generator, List, Set
file = Path('day_three/reorg/input.txt')

def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()

priority = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    "A": 27,
    "B": 28,
    "C": 29,
    "D": 30,
    "E": 31,
    "F": 32,
    "G": 33,
    "H": 34,
    "I": 35,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 39,
    "N": 40,
    "O": 41,
    "P": 42,
    "Q": 43,
    "R": 44,
    "S": 45,
    "T": 46,
    "U": 47,
    "V": 48,
    "W": 49,
    "X": 50,
    "Y": 51,
    "Z": 52
}

def get_three_rucksacks(input: Generator[str, None, None]):
    rucksacks: List[str] = []
    for rucksack in input:
        rucksacks.append(rucksack)
        if len(rucksacks) == 3:
            yield rucksacks
            rucksacks = []

def find_matching_package(compartment_one:str, compartment_two:str):
    return set(compartment_one).intersection(compartment_two)


def find_matching_package_from_group(group: Generator[List[str], None, None]):
    for rucksacks in group:
        rucksack_iterator = iter(rucksacks)
        yield reduce(find_matching_package, rucksack_iterator, next(rucksack_iterator))

def calculate_priority(matches: Set[str]):
    return sum(priority[package] for package in matches)

def calculate_group_priority(matches: Generator[Set[str], None, None]):
    return [calculate_priority(package) for package in matches]

matching_packages = find_matching_package_from_group(get_three_rucksacks(get_input_data()))
result = sum(calculate_group_priority(matching_packages))
print(result)