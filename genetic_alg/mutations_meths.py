from .heuristics.definitions import *
import random


def invertion_mutation(pieces: list[Piece], all_pieces: list[Piece]) -> list[Piece]:
    '''
        Select a subset of our genes and reverse their order.
        The genes have to be contiguous in this case 

        Parameters:
            -list[Piece]: To mutate
            -list[Piece]: Diferent Pieces
        Return:
            -list[Piece]: Mutated

        Ex:
            pieces=[P1,P2,P3,P4,P5,P6]
            all_pieces=[P1,P2,P3,P4,P5,P6,P7,P8,P9]
    '''
    l = len(pieces)

    if l < 4:
        return pieces

    half = int(l/2)
    size = random.randint(1, half)
    start = random.randint(0, half-1)

    if (last := size+start) >= l:
        last = l-1

    inverted = pieces[start:last]
    inverted.reverse()

    result = pieces[:start]+inverted+pieces[last:]

    return result


def swap_mutation(pieces: list[Piece], all_pieces: list[Piece]) -> list[Piece]:
    '''
        Select two genes from our chromosome and interchange their values.

        Parameters:
            -list[Piece]: To mutate
            -list[Piece]: Diferent Pieces
        Return:
            -list[Piece]: Mutated

        Ex:
            pieces=[P1,P2,P3,P4,P5,P6]
            all_pieces=[P1,P2,P3,P4,P5,P6,P7,P8,P9]
    '''
    l = len(pieces)

    if l < 2:
        return pieces

    if l == 2:
        return pieces[::-1]

    rand1 = random.randint(0, l-1)
    while True:
        rand2 = random.randint(0, l-1)
        if rand2 != rand1:
            break

    temp = pieces[rand1]
    pieces[rand1] = pieces[rand2]
    pieces[rand2] = temp
    return pieces


def resetting_mutation(pieces: list[Piece], all_pieces: list[Piece]) -> list[Piece]:
    '''
        Select one or two genes (array indices) and replace their values 
        with another random value from their given pieces. 

        Parameters:
            -list[Piece]: To mutate
            -list[Piece]: Diferent Pieces
        Return:
            -list[Piece]: Mutated

        Ex:
            pieces=[P1,P2,P3,P4,P5,P6]
            all_pieces=[P1,P2,P3,P4,P5,P6,P7,P8,P9]
            res=[P1,P2,P3,P4,P5,P9]
    '''

    len_pieces = len(pieces)
    len_all_pieces = len(all_pieces)

    rand_pos_all = random.randint(0, len_all_pieces-1)
    rand_pos_piece = random.randint(0, len_pieces-1)
    pieces[rand_pos_piece] = all_pieces[rand_pos_all]

    rand = random.randint(0, 1)
    if rand:
        while True:
            rand2 = random.randint(0, len_pieces-1)
            if rand2 != rand_pos_piece:
                break

        rand_pos_all = random.randint(0, len_all_pieces-1)
        pieces[rand2] = all_pieces[rand_pos_all]

    return pieces
