import re
import random
from itertools import islice
from pathlib import Path
from collections import defaultdict, Counter, deque

from termcolor import cprint


def index_corpus(file):
    model = defaultdict(Counter)
    with file.open() as f:
        for l in f:
            words = l.strip().split()
            for x, y, z in zip([None, None] + words, [None] + words + [None], words + [None, None]):
                model[x, y][z] += 1
    normalized = {}
    for key, c in model.items():
        total = sum(c.values())
        normalized[key] = {w: count / total for w, count in c.items()}
    return normalized


def run_chain(model):
    current = deque([None, None], maxlen=2)
    out = []
    while True:
        possibilities = model[tuple(current)]

        rand = random.random()

        cumulative = 0
        for word, probability in possibilities.items():
            cumulative += probability
            if cumulative > rand:
                break
        if word is None:
            break
        out.append(word)
        current.append(word)
    return ' '.join(out)


def play_game():
    path = Path('newsspace_titles.txt')
    model = index_corpus(path)
    all_titles = {l.strip() for l in path.open(encoding='utf8')}
    while True:
        real = random.randint(0, 2) > 1
        if real:
            phrase = all_titles.pop()
        else:
            phrase = run_chain(model)
            if phrase in all_titles:
                real = True

        cprint(phrase, 'cyan')
        print()

        while True:
            print('Real or fake? [rf] ', end='')
            answer = input().strip()
            if answer in ('r', 'f'):
                break

        if real:
            explanation = 'It was a real headline.'
        else:
            explanation = 'We made it up!'

        if (answer == 'r') == real:
            cprint('Correct! ' + explanation, 'green')
        else:
            cprint('Wrong! ' + explanation, 'red')
        print()



if __name__ == '__main__':
    play_game()
