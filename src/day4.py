from . import get_input_data

TEST_DATA = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def solve(data: list[str]):
    result = 0

    cards_matches = {}
    cards_total = {}

    def updateCardCopies(card: int):
        cards_total[card] += 1
        if cards_matches[card] > 0:
            for x in range(card + 1, card + cards_matches[card] + 1):
                updateCardCopies(x)

    for line in data:
        card_id, numbers = line.split(": ")
        card = int(card_id.split()[1])
        win, have = [[int(x) for x in n.split()] for n in numbers.split(" | ")]

        matched = len(set(win) & set(have))
        result += (2**(matched - 1) if matched > 0 else 0)

        cards_matches[card] = matched
        cards_total[card] = 0

    print (f"Day 4, Step 1: {result}")

    for card in cards_total:
        updateCardCopies(card)

    print (f"Day 4, Step 2: {sum(cards_total.values())}")


if __name__ == "__main__":
    data = get_input_data(4)
    test = TEST_DATA.split("\n")

    solve(data)
