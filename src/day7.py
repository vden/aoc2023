from enum import Enum
from functools import cmp_to_key
from itertools import combinations
from typing import Union

from . import get_input_data

TEST_DATA = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


class Type(Enum):
    FIVE = 0
    FOUR = 1
    FULL_HOUSE = 2
    THREE = 3
    TWO_PAIR = 4
    PAIR = 5
    ONE = 6


def card2weight(card: str) -> int:
    cards = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
    mapping = {k: v for (v, k) in enumerate(cards)}

    return mapping[card]


def card2weightWithJoker(card: str) -> int:
    cards = ('J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A')
    mapping = {k: v for (v, k) in enumerate(cards)}

    return mapping[card]


def findCombinations(hand: list[int], with_joker: bool = False) -> Type:
    types = {x: (0 if x != Type.ONE else 1) for x in Type}
    work = [(x, idx) for idx, x in enumerate(hand)]

    def findRepeated(card: str, hand: list[int], num: int) -> Union[tuple[Type, list[int]], None]:
        res = {5: Type.FIVE, 4: Type.FOUR, 3: Type.THREE, 2: Type.PAIR}
        current = [x for x in hand if x[0] != -1]
        for variant in combinations(current, num):
            if all((x[0] == card) for x in variant):
                return res[num], [x[1] for x in variant]

    cards = set(hand) if not with_joker else range(1, 13)
    for card in cards:
        current = dcurrent = work
        if with_joker:
            # replace joker (value = 0) with the current card
            current = [((card, idx) if x == 0 else (x, idx)) for (x, idx) in work]

        local = {x: (0 if x != Type.ONE else 1) for x in Type}
        for ncard in range(0, 13):
            # iterate over every possible card to find all combinations in the current hand
            dcurrent = current[:]
            for num in range(5, 1, -1):
                res = findRepeated(ncard, dcurrent, num)
                # print (f"Try {num}: got {res}")
                if res:
                    found, positions = res
                    for pos in positions:
                        dcurrent[pos] = (-1, pos)

                    local[found] += 1

        if local[Type.THREE] == 1 and local[Type.PAIR] == 1:
            types[Type.FULL_HOUSE] = 1
        elif local[Type.PAIR] == 2:
            types[Type.TWO_PAIR] = 1
        else:
            local_high = sorted([k.value for (k, v) in local.items() if v > 0])[0]
            types[Type(local_high)] = 1

    highest = sorted([k.value for (k, v) in types.items() if v > 0])[0]
    return Type(highest)


def order(a: tuple[Type, list[int], int], b: tuple[Type, list[int], int]) -> int:
    if a[0] != b[0]:
        return 1 if b[0].value < a[0].value else -1
    else:
        for i in range(0, 6):
            if a[1][i] != b[1][i]:
                return 1 if b[1][i] > a[1][i] else -1

        return 0


def solve(data: list[str]):
    _hands, bids = zip(*[x.split() for x in data])
    bids = [int(x) for x in bids]

    # step 1, all cards are what they are
    hands = [[card2weight(k) for k in x] for x in _hands]
    tops = []

    for idx, hand in enumerate(hands):
        combination = findCombinations(hand)
        tops.append((combination, hand, idx))

    tops.sort(key=cmp_to_key(order), reverse=True)
    wins = [bids[x[2]] * (idx + 1) for idx, x in enumerate(tops)]

    print (f"Day 7, Step 1: {sum(wins)}")

    # step 2, J is now Joker
    hands = [[card2weightWithJoker(k) for k in x] for x in _hands]
    tops = []

    for idx, hand in enumerate(hands):
        combination = findCombinations(hand, with_joker=True)
        tops.append((combination, hand, idx))

    tops.sort(key=cmp_to_key(order), reverse=True)
    wins = [bids[x[2]] * (idx + 1) for idx, x in enumerate(tops)]

    print (f"Day 7, Step 2: {sum(wins)}")


if __name__ == "__main__":
    test = TEST_DATA.split("\n")
    data = get_input_data(7)

    solve(data)