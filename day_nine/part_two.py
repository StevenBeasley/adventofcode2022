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


def is_on_same_axis(one: Coordinates, two: Coordinates) -> bool:
    return one[0] == two[0] or one[1] == two[1]


class Machine:
    matrix: List[List[MatrixPoint]]
    lengths: List[Coordinates]

    def __init__(self, lengths) -> None:
        # create an initial matrix of 5 x 5 (to make starting easy)
        matrix: List[List[bool]] = []

        for x in range(5):
            new_x = []
            for y in range(5):
                new_x.append(starting_state)
            matrix.append(new_x)
        self.matrix = matrix

        # set start to the middle
        self.lengths = [Coordinates(2, 2) for x in range(lengths)]

        self.set_tail_positions_as_visited()

    def add_right(self):
        # add a row to the left
        for row in self.matrix:
            row.append(starting_state)

    def add_left(self):
        # add a row to the left
        for row in self.matrix:
            row.insert(0, starting_state)
        # move the x positions right 1
        for i, _ in enumerate(self.lengths):
            self.lengths[i] = Coordinates(
                self.lengths[i][0] + 1, self.lengths[i][1])

    def set_tail_positions_as_visited(self):
        tail_position = self.lengths[-1:][0]
        self.matrix[tail_position[1]][tail_position[0]] = True

    def add_top(self):
        # add a row to the top
        current_width, _ = matrix_dimensions(self.matrix)
        new_row = [starting_state for x in range(current_width)]
        self.matrix.insert(0, new_row)
        # move the y positions down 1
        for i, _ in enumerate(self.lengths):
            self.lengths[i] = Coordinates(
                self.lengths[i][0], self.lengths[i][1] + 1)

    def add_bottom(self):
        # add a row to the bottom
        current_width, _ = matrix_dimensions(self.matrix)
        new_row = [starting_state for x in range(current_width)]
        self.matrix.append(new_row)

    def move_head(self, command):
        head = self.lengths[0]
        if command == 'U':
            # move up
            head = Coordinates(head[0], head[1] - 1)
        elif command == 'D':
            # move down
            head = Coordinates(head[0], head[1] + 1)
        elif command == 'L':
            # move left
            head = Coordinates(head[0] - 1, head[1])
        elif command == 'R':
            # move right
            head = Coordinates(head[0] + 1, head[1])
        self.lengths[0] = head

    def assess_spare_room(self):
        head = self.lengths[0]
        current_width, current_height = matrix_dimensions(self.matrix)
        # we want to make sure there is one extra space on any side of the head
        if head[0] == 0:
            self.add_left()
        if head[0] == current_width - 1:
            self.add_right()

        if head[1] == 0:
            self.add_top()
        if head[1] == current_height - 1:
            self.add_bottom()

    def assess_tail_position(self, tail_index: int):
        head = self.lengths[tail_index - 1]
        tail = self.lengths[tail_index]

        command_movement = {
            'U': -1,
            'D': 1,
            'L': -1,
            'R': 1
        }
        # make sure tail is within one space of head
        if head[0] > tail[0] + 1:
            if is_on_same_axis(head, tail):
                # head has moved too far right
                tail = Coordinates(tail[0] + 1, tail[1])
            else:
                # head has moved diagnally right
                tail = Coordinates(head[0] - 1, head[1])
        if head[0] < tail[0] - 1:
            if is_on_same_axis(head, tail):
                # head has moved too far left
                tail = Coordinates(tail[0] - 1, tail[1])
            else:
                # head has moved diagnally left
                tail = Coordinates(head[0] + 1, head[1])

        if head[1] > tail[1] + 1:
            if is_on_same_axis(head, tail):
                # head has moved too far down
                tail = Coordinates(tail[0], tail[1] + 1)
            else:
                # head has moved diagnally up
                tail = Coordinates(head[0], head[1] - 1)

        if head[1] < tail[1] - 1:

            if is_on_same_axis(head, tail):
                # head has moved too far up
                tail = Coordinates(tail[0], tail[1] - 1)
            else:
                # head has moved diagnally up, move under it
                tail = Coordinates(head[0], head[1] + 1)

        self.lengths[tail_index] = tail

    def submit_command(self, command: Command):
        for _ in range(command[1]):
            self.move_head(command[0])
            for i, _ in enumerate(self.lengths):
                # skip the head
                if i > 0:
                    self.assess_tail_position(i)

            self.set_tail_positions_as_visited()
            self.assess_spare_room()
            # self.print_state(command)

    def get_tail_visited(self):
        def count_x(row):
            return sum([1 for x in row if x])
        return sum([count_x(row) for row in self.matrix])

    def matrix_with_rope(self):
        # need to de-reference
        new_matrix = deepcopy(self.matrix)
        lengths = deepcopy(self.lengths)
        for i in range(len(lengths) - 1, -1, -1):
            if i == 0:
                # set H
                new_matrix[lengths[i][1]][lengths[i][0]] = 'H'
            else:
                # set T
                new_matrix[lengths[i][1]][lengths[i][0]] = str(i)
        return new_matrix

    def print_state(self, command):
        print(
            f'Command({command[0]} {command[1]}))')
        for row in self.matrix_with_rope():
            def char(x):
                if x == 'H':
                    return 'H'
                if x == True:
                    return '#'
                if x == False:
                    return '.'
                else:
                    return x
            print(''.join([char(x) for x in row]))


machine = Machine(10)

for command in parse_input(get_input_data()):
    machine.submit_command(command)
    # machine.print_state(command)
    continue

machine.print_state(command)
print(machine.get_tail_visited())
