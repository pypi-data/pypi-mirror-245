import json
from functools import lru_cache
from pathlib import Path
from random import randint
from typing import List

BASE_DIR = Path(__file__).parent


@lru_cache
def nn():
    with open(BASE_DIR / "weights.json") as fp:
        weights = json.load(fp)

    with open(BASE_DIR / "weights2.json") as fp:
        weights2 = json.load(fp)

    letters: List[List[float]] = []
    letters2: List[List[List[float]]] = []

    for i in range(26):
        cvar = 0
        tvar = 0
        letters.append([])
        for j in range(26):
            cvar += weights[i][j]
        for j in range(26):
            tvar += weights[i][j]
            try:
                letters[i].append((tvar / cvar) * 1000)
            except ZeroDivisionError:
                letters[i].append(0)

    for h in range(26):
        letters2.append([])
        for i in range(26):
            cvar = 0
            tvar = 0
            letters2[h].append([])
            for j in range(26):
                cvar += weights2[h][i][j]

            for j in range(26):
                tvar += weights2[h][i][j]
                try:
                    letters2[h][i].append((tvar / cvar) * 1000)
                except ZeroDivisionError:
                    letters2[h][i].append(0)

    return letters, letters2


def generate_name(min_length: int = 4, max_length: int = 10) -> str:
    try:
        length = randint(min_length, max_length)
        letters, letters2 = nn()

        # first character
        first_char = randint(0, 26)
        name = chr(97 + first_char).upper()

        # second character
        ran = randint(0, 1000)
        secondchar = 0
        curar = letters[first_char]
        while ran >= curar[secondchar]:
            secondchar += 1
        name += chr(97 + secondchar)

        # rest of the characters
        for _ in range(2, length):
            ran = randint(0, 1000)
            nextchar = 0
            curar = letters2[first_char][secondchar]
            while ran >= curar[nextchar]:
                nextchar += 1
            first_char = secondchar
            secondchar = nextchar
            name += chr(97 + nextchar)
        return name
    except IndexError:
        return generate_name(min_length, max_length)
