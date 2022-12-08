from pathlib import Path
from typing import List, Set
file = Path('day_six/input.txt')


def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def generate_next_input(current: str, next_char: str):
    return ''.join([current[-3:], next_char])


def is_marker_unique(marker: str) -> bool:
    return len(set(marker)) == 4


def find_end_of_packet_marker(input: str) -> int:
    start_of_packet_marker = ''
    for index, character in enumerate(input):
        start_of_packet_marker = generate_next_input(
            start_of_packet_marker, character)
        if len(start_of_packet_marker) == 4 and is_marker_unique(start_of_packet_marker):
            # need to return the character after the marker
            return index + 1


for row in get_input_data():
    print(find_end_of_packet_marker(row))
