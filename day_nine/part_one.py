from collections import namedtuple
from typing import Dict, Generator, List, Any, Tuple, TypedDict
from functools import reduce
from pathlib import Path
from copy import deepcopy

file = Path('day_nine/input.txt')

MatrixPoint = namedtuple('MatrixPoint', ['t_been'])
Coordinates = namedtuple('Coordinates', ['x', 'y'])
Command = namedtuple('Command', ['direction', 'count'])
starting_state = False


class Positions(TypedDict):
    head: Coordinates
    tail: Coordinates


def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def parse_input(input: Generator[str, None, None]):
    for line in input:
        commands = line.split(' ')
        yield Command(commands[0], int(commands[1]))


def matrix_dimensions(matrix: List[List[MatrixPoint]]):
    current_width = len(matrix[0])
    current_height = len(matrix)
    return current_width, current_height


class Machine:
    matrix: List[List[MatrixPoint]]
    head: Coordinates
    tail: Coordinates

    def __init__(self) -> None:
        # create an initial matrix of 5 x 5 (to make starting easy)
        matrix: List[List[bool]] = []

        for x in range(5):
            new_x = []
            for y in range(5):
                new_x.append(starting_state)
            matrix.append(new_x)
        self.matrix = matrix

        # set start to the middle
        self.head = Coordinates(2, 2)
        self.tail = Coordinates(2, 2)

        self.set_tail_position_as_visited()

    def add_right(self):
        # add a row to the left
        for row in self.matrix:
            row.append(starting_state)

    def add_left(self):
        # add a row to the left
        for row in self.matrix:
            row.insert(0, starting_state)
        # move the x positions right 1
        self.head = Coordinates(self.head[0] + 1, self.head[1])
        self.tail = Coordinates(self.tail[0] + 1, self.tail[1])

    def set_tail_position_as_visited(self):
        tail_position = self.tail
        self.matrix[tail_position[1]][tail_position[0]] = True

    def add_top(self):
        # add a row to the top
        current_width, _ = matrix_dimensions(self.matrix)
        new_row = [starting_state for x in range(current_width)]
        self.matrix.insert(0, new_row)
        # move the y positions down 1
        self.head = Coordinates(self.head[0], self.head[1] + 1)
        self.tail = Coordinates(self.tail[0], self.tail[1] + 1)

    def add_bottom(self):
        # add a row to the bottom
        current_width, _ = matrix_dimensions(self.matrix)
        new_row = [starting_state for x in range(current_width)]
        self.matrix.append(new_row)

    def move_head(self, command):
        if command == 'U':
            # move up
            self.head = Coordinates(self.head[0], self.head[1] - 1)
        elif command == 'D':
            # move down
            self.head = Coordinates(self.head[0], self.head[1] + 1)
        elif command == 'L':
            # move left
            self.head = Coordinates(self.head[0] - 1, self.head[1])
        elif command == 'R':
            # move right
            self.head = Coordinates(self.head[0] + 1, self.head[1])

    def assess_spare_room(self):
        current_width, current_height = matrix_dimensions(self.matrix)
        # we want to make sure there is one extra space on any side of the head
        if self.head[0] == 0:
            self.add_left()
        if self.head[0] == current_width - 1:
            self.add_right()

        if self.head[1] == 0:
            self.add_top()
        if self.head[1] == current_height - 1:
            self.add_bottom()

    def assess_tail_position(self, original_head_position: Command):
        # make sure tail is within one space of head
        # check X axis first
        if self.head[0] > self.tail[0] + 1:
            # head has moved too far right
            self.tail = original_head_position
        if self.head[0] < self.tail[0] - 1:
            # head has moved too far left
            self.tail = original_head_position
        if self.head[1] > self.tail[1] + 1:
            # head has moved too far down
            self.tail = original_head_position
        if self.head[1] < self.tail[1] - 1:
            # head has moved too far up
            self.tail = original_head_position

    def submit_command(self, command: Command):
        for _ in range(command[1]):
            original_head_position = deepcopy(self.head)
            self.move_head(command[0])
            self.assess_tail_position(original_head_position)
            self.set_tail_position_as_visited()
            self.assess_spare_room()
            # self.print_state(command)

    def get_tail_visited(self):
        def count_x(row):
            return sum([1 for x in row if x])
        return sum([count_x(row) for row in self.matrix])

    def matrix_with_rope(self):
        # need to de-reference
        new_matrix = deepcopy(self.matrix)

        # set H
        new_matrix[self.head[1]][self.head[0]] = 'H'
        # set T
        new_matrix[self.tail[1]][self.tail[0]] = 'T'
        return new_matrix

    def print_state(self, command):
        print(
            f'Command({command[0]} {command[1]}) Head({self.head[0]}:{self.head[1]}) Tail({self.tail[0]}:{self.tail[1]})')
        for row in self.matrix_with_rope():
            def char(x):
                if x in ['H', 'T']:
                    return x
                if x:
                    return '#'
                else:
                    return '.'
            print(''.join([char(x) for x in row]))


machine = Machine()

for command in parse_input(get_input_data()):
    machine.submit_command(command)
    # machine.print_state(command)
    continue

machine.print_state(command)
print(machine.get_tail_visited())
