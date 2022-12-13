from typing import Dict, Generator, List, Any, Tuple
from functools import reduce
from pathlib import Path

file = Path('day_eight/input.txt')


def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def generate_input(current_state: List[List[int]], next_row: str):
    current_state.append([int(x) for x in next_row])
    return current_state


def is_bigger(tree_height: int, other_tree_heights: List[int]):
    return tree_height > max(other_tree_heights)


def is_tree_visible(state: List[List[int]], tree_position: Tuple[int, int]) -> bool:
    x = tree_position[0]
    y = tree_position[1]
    # Assume perfect rectangle
    max_x = len(state[0]) - 1
    max_y = len(state) - 1
    if (
        x == 0 or
        x == max_x or
        y == 0 or
        y == max_y
    ):
        # This is an edge, so always visible
        return True
    tree_height = state[y][x]

    left_trees = state[y][:x]
    right_trees = state[y][x + 1:]
    up_down = [row[x] for row in state]
    up_trees = up_down[:y]
    down_trees = up_down[y + 1:]

    return any([
        is_bigger(tree_height, left_trees),
        is_bigger(tree_height, right_trees),
        is_bigger(tree_height, up_trees),
        is_bigger(tree_height, down_trees)
    ])


state = reduce(generate_input, get_input_data(), [])

visible_trees = []
for x in range(len(state[0])):
    for y in range(len(state)):
        coordinates = (x, y)
        if is_tree_visible(state, coordinates):
            visible_trees.append((x, y))
print(f'Visible trees: {len(visible_trees)}')
