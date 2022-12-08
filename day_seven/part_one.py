from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, List, Any, Tuple
file = Path('day_seven/input.txt')


@dataclass()
class Command:
    command: List[str]
    output: List[str]


@dataclass()
class Folder:
    name: str
    size: int
    sub_folders: Dict[str, Any]
    files: List[Tuple[str, int]]


def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def split_commands(input: Generator[str, None, None]) -> List[Command]:
    commands = []
    # get the initial command
    current_command: Command = Command(next(input).split(' ')[1:], [])
    for line in input:
        if line.startswith('$'):
            # all commands
            commands.append(current_command)
            current_command = Command([], [])
            current_command.command = line.split(' ')[1:]
        else:
            # is command output
            current_command.output.append(line)
    return commands


def generate_empty_folder(name: str):
    return Folder(name, 0, {}, [])


def get_folder(current_position: List[str], file_structure: Folder):
    current_folder = file_structure
    for folder in current_position:
        if folder == '/':
            # skip the initial folder
            continue
        current_folder = current_folder.sub_folders[folder]
    return current_folder


def add_new_folder(file_structure: Folder,
                   current_position: List[str], name: str) -> Folder:
    current_folder = get_folder(current_position, file_structure)
    current_folder.sub_folders[name] = generate_empty_folder(name)
    return file_structure


def add_file(current_position: List[str], file_structure: Folder, file: str):
    folder = get_folder(current_position, file_structure)
    size, name = file.split(' ')
    folder.files.append((name, int(size)))


def generate_file_structure(commands: List[Command]):
    file_structure: Folder
    current_position: List[str]

    for command in commands:
        if command.command[0] == 'cd' and command.command[1] == '/':
            # is the start, create the base
            file_structure = generate_empty_folder(command.command[1])
            current_position = ['/']
        elif command.command[0] == 'cd':
            if command.command[1] == '..':
                # dont go below base folder
                if len(current_position) > 1:
                    # going back a folder
                    current_position.pop()
            else:
                # moving to another folder
                name = command.command[1]
                file_structure = add_new_folder(
                    file_structure, current_position, name)
                current_position.append(name)

        elif command.command[0] == 'ls':
            # populate the current folders items
            for file in command.output:
                # skip directories
                if file.startswith('dir'):
                    continue
                add_file(current_position, file_structure, file)
        else:
            print(f'a new command! {command.command[0]}')

    return file_structure


def get_file_sizes(folder: Folder):
    size = 0
    for file in folder.files:
        size += file[1]
    return size


def get_sub_folder_sizes(folder: Folder):
    size = 0
    for sub_folder in folder.sub_folders.values():
        sub_folder_size = 0
        sub_folder_size += get_file_sizes(sub_folder)
        sub_folder_size += get_sub_folder_sizes(sub_folder)
        sub_folder.size = sub_folder_size
        size += sub_folder_size
    return size


def calculate_size(file_structure: Folder):
    files_size = get_file_sizes(file_structure)
    sub_folder_size = get_sub_folder_sizes(file_structure)

    file_structure.size = files_size + sub_folder_size


def sum_folder_and_sub_folders(file_structure: Folder, folder_sizes: List[int]):
    size = file_structure.size
    sub_folder_sizes = []
    for folder in file_structure.sub_folders.values():
        sub_size, sub_list = sum_folder_and_sub_folders(folder, folder_sizes)
        sub_folder_sizes = [*sub_folder_sizes, *sub_list, sub_size]
        size += sub_size
    return size, sub_folder_sizes


commands = split_commands(get_input_data())
file_structure = generate_file_structure(commands)
calculate_size(file_structure)


total_size, individual_sizes = sum_folder_and_sub_folders(file_structure, [])
total = sum([x for x in individual_sizes if x <= 100000])
print(total)

# print(file_structure)
