import re
from dataclasses import dataclass

from . import get_input_data

TEST_DATA = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


@dataclass
class Play:
    red: int = 0
    green: int = 0
    blue: int = 0


def solve(data: list[str]):
    total = 0
    total_powers = 0

    for line in data:
        game_n, plays = line.split(":")
        game_round = int(re.sub("[^0-9]", "", game_n))
        failed = False

        # print (f"Game {game_round}")
        min_set = Play()

        for _play in plays.split(";"):
            vars = {}
            for m in re.finditer("(\\d+) (red|blue|green)", _play):
                num, kind = m.groups()
                vars[kind] = int(num)
            play = Play(**vars)

            if play.red > 12 or play.green > 13 or play.blue > 14:
                failed = True

            min_set.red = max(min_set.red, play.red)
            min_set.green = max(min_set.green, play.green)
            min_set.blue = max(min_set.blue, play.blue)

        if not failed:
            total += game_round

        total_powers += (min_set.red * min_set.green * min_set.blue)

    print (f"Day 2, Step 1: {total}")
    print (f"Day 2, Step 2: {total_powers}")


if __name__ == "__main__":
    data = get_input_data(2)
    test = TEST_DATA.split("\n")

    solve(data)