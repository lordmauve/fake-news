import re
import random
from pathlib import Path
from collections import defaultdict, Counter, deque

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



if __name__ == '__main__':
    path = Path('phrases.txt')
    model = index_corpus(path)
    for _ in range(10):
        print(run_chain(model))
