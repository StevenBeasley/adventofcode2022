from enum import Enum
from pathlib import Path
file = Path('day_two/rock_paper_scisors/input.txt')

def get_input_data():
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()

class Points(Enum):
    PAPER:int = 2
    SCISORS:int  = 3
    ROCK:int  = 1
    WIN:int  = 6
    LOSS:int  = 0
    DRAW:int  = 3

play_map = {
    'A': Points.ROCK,
    'B': Points.PAPER,
    'C': Points.SCISORS,
    'X': Points.LOSS,
    'Y': Points.DRAW,
    'Z': Points.WIN,
}

def get_plays(input_data: str):
    player_one = input_data[:1]
    result = input_data[-1:]

    return play_map[player_one], play_map[result]

def determine_round_points(player_one: Points, result: Points):
    if result == Points.DRAW:
        return player_one.value + Points.DRAW.value

    if player_one == Points.PAPER:
        if result == Points.WIN:
            return Points.WIN.value + Points.SCISORS.value
        if result == Points.LOSS:
            return Points.LOSS.value + Points.ROCK.value

    if player_one == Points.SCISORS:
        if result == Points.WIN:
            return Points.WIN.value + Points.ROCK.value
        if result == Points.LOSS:
            return Points.LOSS.value + Points.PAPER.value

    if player_one == Points.ROCK:
        if result == Points.WIN:
            return Points.WIN.value + Points.PAPER.value
        if result == Points.LOSS:
            return Points.LOSS.value + Points.SCISORS.value

result = sum([determine_round_points(*x) for x in (get_plays(x) for x in get_input_data())])
print(result)