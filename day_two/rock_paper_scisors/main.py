
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
    'X': Points.ROCK,
    'Y': Points.PAPER,
    'Z': Points.SCISORS,
}

def determine_round_points(player_one: Points, player_two: Points):
    player_one_points:int = player_one.value
    player_two_points:int = player_two.value

    if player_one == player_two:
        player_one_points += Points.DRAW.value
        player_two_points += Points.DRAW.value

    if player_one == Points.PAPER and player_two == Points.SCISORS:
        player_two_points += Points.WIN.value
    if player_one == Points.PAPER and player_two == Points.ROCK:
        player_one_points += Points.WIN.value

    if player_one == Points.SCISORS and player_two == Points.PAPER:
        player_one_points += Points.WIN.value
    if player_one == Points.SCISORS and player_two == Points.ROCK:
        player_two_points += Points.WIN.value
    
    if player_one == Points.ROCK and player_two == Points.PAPER:
        player_two_points += Points.WIN.value
    if player_one == Points.ROCK and player_two == Points.SCISORS:
        player_one_points += Points.WIN.value

    return player_one_points, player_two_points

def get_plays(input_data: str):
    player_one = input_data[:1]
    player_two = input_data[-1:]

    return play_map[player_one], play_map[player_two]

if __name__ == "__main__":
    player_one_total: int = 0
    player_two_total: int = 0
    # res = [x for x in determine_round_points(x) for x in (get_plays(x) for x in get_input_data()))]
    for player_one_points, player_two_points in (determine_round_points(*x) for x in (get_plays(x) for x in get_input_data())):
        
        player_one_total += player_one_points
        player_two_total += player_two_points
    
    print(player_one_total)
    print(player_two_total)
