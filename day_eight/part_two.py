from typing import Dict, Generator, List, Any, Tuple
from math import prod
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


def trees_from_coordinates(state: List[List[int]], tree_position: Tuple[int, int]) -> bool:
    x = tree_position[0]
    y = tree_position[1]
    left_trees = state[y][:x]
    left_trees.reverse()
    right_trees = state[y][x + 1:]
    up_down = [row[x] for row in state]
    up_trees = up_down[:y]
    up_trees.reverse()
    down_trees = up_down[y + 1:]

    return [left_trees, right_trees, up_trees, down_trees]


def calculate_score(tree_height: int, possible_trees: List[List[int]]):
    score = []
    for row in possible_trees:
        if len(row) == 0:
            score.append(0)
            continue
        for index, tree in enumerate(row):
            if tree >= tree_height:
                score.append(index + 1)
                break
            if index == len(row) - 1:
                score.append(index + 1)

    return prod(score)


state = reduce(generate_input, get_input_data(), [])

max_score = 0
for x in range(len(state[0])):
    for y in range(len(state)):
        coordinates = (x, y)
        tree_height = state[y][x]
        possible_trees = trees_from_coordinates(state, coordinates)
        score = calculate_score(tree_height, possible_trees)
        if score > max_score:
            max_score = score

print(f'Best scenic score: {max_score}')
