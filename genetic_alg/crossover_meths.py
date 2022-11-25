from .heuristics.definitions import *
import random


def single_point_crossover(parent1: list[Piece], parent2: list[Piece], subject_len: int, all_pieces: list[Subject]) -> list[Piece]:
    '''
        A crossover point on the parent organism is selected.
        All data beyond that point in the organism string is swapped between the two parent organisms.

        Parameters:
            -stock_area: the area of the stock
            -stock_space: the space needed between pieces
            -parent1 :List of pieces of the first parent
            -parent2 :List of pieces of the first parent
        Return:
            -child: :List of pieces resulting of combining both parents

        Ex:
            parent1=[P1,P2,P3,P4]
            parent2=[P5,P6,P3,P7]

            child1=[P1,P2,P3,P7]
            child2=[P5,P6,P3,P4]
    '''

    min_len: int = min(len(parent1), len(parent2))

    # Crossover point have no sense
    if min_len <= 1:
        first = random.randint(0, 1)
        if first:
            return parent1+parent2
        return parent2+parent1

    parents: list[list[Piece]] = [parent1, parent2]
    new_chromosome_pieces: list[Piece] = []

    half = int(min_len/2)
    first = random.randint(0, 1)
    crossover_point = random.randint(half, min_len-1)

    first_pieces: list[Piece] = parents[first][:crossover_point]
    first_rest: list[Piece] = parents[first][crossover_point:]

    first = 1-first

    last_pieces: list[Piece] = parents[first][crossover_point:]
    last_rest: list[Piece] = parents[first][:crossover_point]

    first = random.randint(0, 1)
    if first:
        rest = first_rest+last_rest
    else:
        rest = last_rest+first_rest

    new_chromosome_pieces: list[Piece] = first_pieces+last_pieces+rest

    needed = subject_len - len(new_chromosome_pieces)
    for _ in range(needed):
        rand = random.randint(0, len(all_pieces)-1)
        new_chromosome_pieces.append(all_pieces[rand])

    return new_chromosome_pieces


def two_point_crossover(stock_area: int, stock_space: int, parent1: list[Piece], parent2: list[Piece]) -> list[Piece]:
    '''
        Two random points are chosen on the individual chromosomes and the genetic material is exchanged
        at these points.

        Parameters:
            -stock_area: the area of the stock
            -stock_space: the space needed between pieces
            -parent1 :List of pieces of the first parent
            -parent2 :List of pieces of the first parent
        Return:
            -child: :List of pieces resulting of combining both parents

        Ex:
            parent1=[P1,P2,P3,P4]
            parent2=[P5,P6,P3,P7]

            child1=[P1,P6,P3,P4]
            child2=[P5,P2,P3,P7]
    '''

    min_len: int = min(len(parent1), len(parent2))
    parents: list[list[Piece]] = [parent1, parent2]

    new_chromosome_pieces: list[Piece] = []

    first = random.randint(0, 1)
    half = int(min_len/2)

    crossover_point1 = random.randint(0, half-1)
    crossover_point2 = random.randint(half, min_len-1)

    first_parent: list[Piece] = parents[first]
    first = 1-first
    last_parent: list[Piece] = parents[first]

    new_chromosome_pieces: list[Piece] = first_parent[:crossover_point1] + \
        last_parent[crossover_point1:crossover_point2] + \
        first_parent[crossover_point2:]

    return new_chromosome_pieces


def uniform_crossover(stock_area: int, stock_space: int, parent1: list[Piece], parent2: list[Piece]) -> list[Piece]:
    '''
        Each gene is selected randomly from one of the corresponding genes of the parent chromosomes.

        Parameters:
            -stock_area: the area of the stock that is being used
            -stock_space: the space needed between pieces
            -parent1 :List of pieces of the first parent
            -parent2 :List of pieces of the first parent
        Return:
            -child: :List of pieces resulting of combining both parents

        Ex:
            parent1=[P1,P2,P3,P4]
            parent2=[P5,P6,P3,P7]
            child=[P1|P5,P2|P6,P3,P4|P7]    
    '''

    min_len: int = min(len(parent1), len(parent2))
    parents: list[list[Piece]] = [parent1, parent2]

    new_chromosome_pieces: list[Piece] = []

    for index in range(min_len):
        rand = random.randint(0, 1)
        piece = parents[rand][index]

        stock_area -= piece.area_with_space(stock_space)

        if stock_area:
            new_chromosome_pieces.append(piece)
        else:
            break

    # Check this
    if stock_area <= 0:
        return new_chromosome_pieces

    max_parent = parent1 if len(parent1) == min_len else parent2
    index = min_len

    while stock_area and index < len(max_parent):
        piece = max_parent[index]
        stock_area -= piece.area_with_space(stock_space)

        if stock_area:
            new_chromosome_pieces.append(piece)

        index += 1

    return new_chromosome_pieces
