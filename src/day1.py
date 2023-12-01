from . import get_input_data


def solve(data: list[str]):
    res = 0
    for line in data:
        digits = [x for x in line if x.isdigit()]
        number = int(digits[0] + digits[-1])
        res += number
    print (f"Day 1, Step 1: {res}")


def solve2(data: list[str]):
    res = 0
    digits_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    for line in data:
        digits = ""
        while line:
            if line[0].isdigit():
                digits += line[0]
                line = line[1:]
                continue

            for (k, v) in digits_map.items():
                if line.startswith(k):
                    digits += v
                    break
            line = line[1:]

        number = int(digits[0] + digits[-1])
        res += number

    print (f"Day 1, Step 2: {res}")


TEST_DATA = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

TEST_DATA2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

if __name__ == "__main__":
    data = get_input_data(1)
    test = TEST_DATA.split("\n")
    test = TEST_DATA2.split("\n")

    solve(data)
    solve2(data)