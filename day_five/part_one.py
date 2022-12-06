from enum import Enum
from pathlib import Path
from typing import Generator, List, Tuple, Union
file = Path('day_five/input.txt')


def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def parse_starting_position(row: str):
    if row.startswith('['):
        chunks = []
        # break the row into 4 character chunks and return each result
        for i in range(0, len(row), 4):
            chunk = row[i+1:i+2]
            if chunk == ' ':
                chunks.append(None)
            else:
                chunks.append(chunk)
        return chunks


def parse_instruction(row: str):
    items = row.split(' ')
    # every second item should be sent back:
    # move 4 from 9 to 8
    #      ^      ^    ^
    return (int(items[1]), int(items[3]), int(items[5]))


def generate_stacks(starting_positions: List[Union[str, None]]):

    # generate empty stacks
    number_of_stacks = len(starting_positions[0])
    stacks = [[] for x in range(number_of_stacks)]

    # move the items onto the correct stack in reverse order (bottom to top)
    for i in range(len(starting_positions) - 1, -1, -1):
        row = starting_positions[i]
        for stack, crate in enumerate(row):
            if crate:
                stacks[stack].append(crate)

    return stacks


def parse_input(input: Generator[str, None, None]):
    starting_positions = []
    instructions = []
    # everything before the first empty row is starting positions
    for line in input:
        if line == '':
            break
        starting_position = parse_starting_position(line)
        if starting_position:
            starting_positions.append(starting_position)

    stacks = generate_stacks(starting_positions)

    # everything after the first empty row is instructions
    for line in input:
        instructions.append(parse_instruction(line))

    return stacks, instructions


def process_instruction(stacks: List[List[str]], instruction: Tuple[int, int, int]):
    quantity = instruction[0]
    start_position = instruction[1] - 1
    end_position = instruction[2] - 1

    for _ in range(quantity):
        # grab the crate from start stack
        crate = stacks[start_position].pop()
        # move to end stack
        stacks[end_position].append(crate)


input_generator = get_input_data()
stacks, instructions = parse_input(input_generator)
for row in stacks:
    print(row)
for instruction in instructions:
    process_instruction(stacks, instruction)
for row in stacks:
    print(row)
# result
print(''.join([x[-1:][0] for x in stacks]))
