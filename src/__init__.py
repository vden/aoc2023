import os

import requests
from dotenv import load_dotenv

load_dotenv()

def get_input_data(day: int) -> list[str]:
    headers = {
        "cookie": f"session={os.environ['AOC_SESSION']}"
    }

    data = requests.get(f"https://adventofcode.com/2023/day/{day}/input", headers=headers)
    return data.text.strip().split("\n")