from genetic_alg.main import main as m1
from geocuba_alg.main import main as m2
from random_alg.main import main as m3
from ffd_cut_alg.main import main as m4

import random

# CONSTANTS
HEIGHT = 700
WIDTH = 500
MAX_ELEMENTS = 20
MIN_DEMAND = 500
MAX_DEMAND = 1000


def gen_vectors(len: int = 20):
    """Generate a list of tags with the follow format:
    ((id, width, height), demand) where
    id: unique integer
    width: integer between 1 and and 250
    height: integer between 1 and and 350
    demand: integer between 1000 and and 50000

    Args:
        len (int, optional): Amount of items. Defaults to 20.

    Returns:
        list: list of tuples
    """
    # Generate random ids between 1 and 30
    ids = random.sample(range(1, len+1), len)
    lw = random.sample(range(1, int(WIDTH/2)), len)
    lh = random.sample(range(1, int(HEIGHT/2)), len)
    ld = random.sample(range(MIN_DEMAND, MAX_DEMAND), len)

    vector = [((ids[i], lw[i], lh[i]), ld[i]) for i in range(len)]
    total_demand = sum(ld)

    inc_number = random.randint(0, round(len/2))
    incompatible = []
    for _ in range(inc_number):
        first = random.sample(ids, 1)
        n_ids = ids.copy()
        n_ids.remove(first[0])
        second = random.sample(n_ids, 1)
        incompatible.append((first[0], second[0]))

    return vector, incompatible, total_demand

def main():
    f = open('output.txt', 'a')
    it = 1
    for i in range(10, 21):
        print(f'{i}')
        for _ in range(1):
            vector, incompatible, total = gen_vectors(i)
            l = set(incompatible)
            w1, _, t1 = m1(pieces_list=vector,
                           incompatible=incompatible)
            print('f')
            w2, _, t2 = m2(pieces_list=vector,
                           incompatible=incompatible)
            print('f')
            w3, _, t3 = m3(pieces_list=vector,
                           incompatible=incompatible)
            print('f')
            w4, p,t4 = m4(pieces_list=vector, incompatible=incompatible)
            print('f')
            f.write(
                f'{it}. {i}. {total}. {len(l)}. {w1}. {t1}. {w2}. {t2}. {w3}. {t3}. {w4}. {t4}\n')
            it += 1
    f.close()

if __name__=="__main__":
    main()