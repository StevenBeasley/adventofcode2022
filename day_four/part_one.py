from pathlib import Path
from typing import List, Set, Tuple
file = Path('day_four/input.txt')

def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()

def parse_input(input: str):
    
    split = input.split(',')

    work_assignments: List[Tuple[int, int]] = []
    for assignemnt in split:
        elf_work_assignments = assignemnt.split('-')
        work_assignments.append((int(elf_work_assignments[0]), int(elf_work_assignments[1])))
    return work_assignments

def is_either_contained(assignment_one: Tuple[int, int], assignment_two: Tuple[int, int]):
    assignment_one_full = set(range(assignment_one[0], assignment_one[1] + 1))
    assignment_two_full = set(range(assignment_two[0], assignment_two[1] + 1))

    if assignment_one_full.issubset(assignment_two_full) or assignment_two_full.issubset(assignment_one_full):
        return True
    return False

complete_overlaps = 0
for x in get_input_data():
    if is_either_contained(*parse_input(x)):
        complete_overlaps += 1

print(complete_overlaps)
