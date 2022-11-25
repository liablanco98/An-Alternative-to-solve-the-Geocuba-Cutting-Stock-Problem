from .heuristics.definitions import *
from .random_alg import Random_A


def receive_input(pieces_list: list[tuple[tuple[int, int, int], int]], dict_incompatible: dict[int, set], sheet: tuple[int, int], space: int) -> Stock:
    '''
        Parameters:
            - pieces: list of tuple ((piece id, length, piece width),piece demand)
            - dict_incompatible: a dictionary[int,set] that gives the set of pieces that cannot be colocated next to the piece id
            - sheet: tuple (sheet length, sheet width)
            - space: an int with the space that most be left between sheets
    '''
    # Buiding the pieces_list
    pieces: list[tuple[Piece, int]] = []
    for val, demand in pieces_list:
        id = val[0]
        length = val[1]
        width = val[2]
        incompatible = dict_incompatible.get(id, set())
        pieces.append((Piece(id, length, width, incompatible), demand))

    return Stock(length=sheet[0], width=sheet[1], pieces=pieces, space=space)


def ret_output(stock: Stock, skip: bool, function_type: int, iterations_count: int, population_size: int):
    '''
        Parameters:
            - the stock: contains the dimensions of the sheets and the pieces to be produced
        Return:
            - the total waste of using all patterns obtained
            - the result patterns and times to be used
                -pattern: (pattern waste, pattern placement, used pieces)
                    -pattern waste: the waste of that pattern
                    -pattern placement: (initial position, last position, piece id)
                    -used pieces: list (piece id, number of times used)
    '''
    genetic = Random_A(stock, skip, function_type,
                       iterations_count, population_size)
    best_score, best_subjects, subjects_counter, time = genetic.run()

    def get_index(lis, elem) -> int:
        '''
            Gives the position of an element into a list if exists
            Else returns -1
        '''
        if not len(lis):
            return -1
        for index in range(len(lis)):
            if lis[index] == elem:
                return index
        return -1

    list_patterns: list[tuple[tuple[int, list[tuple[tuple[int, int],
                                                    tuple[int, int], int]], list[tuple[int, int]]], int]] = []

    # Represents the list [(pieces,times)] of each pattern
    pieces_counted: list[list[tuple[Piece, int]]] = []
    for index in range(len(best_subjects)):
        subject: Subject = best_subjects[index]
        count: int = subjects_counter[index]

        third = [(k.id, v) for k, v in subject.pieces_used.items()]
        # Sort to keep order in the answer
        third.sort()
        # From Equivalent Patterns only one is selected and the times= times(patt1)+times(patt2)
        n_index = get_index(pieces_counted, third)
        if n_index != -1:
            tupl = list_patterns[n_index][0]
            val = list_patterns[n_index][1]
            list_patterns[n_index] = (tupl, val+count)
            continue

        second = [(start, last, p.id)
                  for start, last, p in subject.pattern]
        # Sort to keep order in the answer
        second.sort(key=lambda x: x[0])

        first = subject.waste

        list_patterns.append(((first, second, third), count))
        pieces_counted.append(third)

    return best_score, list_patterns, time


def main(pieces_list: list[tuple[tuple[int, int, int], int]], sheet: tuple[int, int] = (700, 500), space: int = 0, incompatible: list[tuple[int, int]] = [], skip: bool = False, funct_type: int = 1, iterations_count: int = 50,  population_size: int = -1):
    '''
        Receives the input and returns the results of applying a genetic solver method for cutting material problem
        Parameters:
            - pieces_list: a list of ((piece id, piece length, piece width), piece demand)
            - sheet: (sheet length, sheet width)
            - space: the space that needs to be maintained between two consecutive pieces
            - incompatible: a list of tuples representing the identifiers of pieces that cannot be placed on the same sheet
        Return:
            - the total waste of using all the selected patterns
            - the patterns:
                - pattern waste
                - the pieces used and the times it is used
                - the position of the pieces
    '''

    # Checking tuple
    new_tuple_list: list[tuple[int, int]] = []
    for first, sec in incompatible:
        tup = (first, sec)
        reverse = (sec, first)
        if tup in new_tuple_list or reverse in new_tuple_list:
            continue
        new_tuple_list.append(tup)

    # Building the incompatible list
    dic_incopat: dict[int, set[int]] = {}
    for first, sec in new_tuple_list:
        first_list = dic_incopat.get(first, set())
        sec_list = dic_incopat.get(sec, set())

        first_list.add(sec)
        dic_incopat[first] = first_list

        sec_list.add(first)
        dic_incopat[sec] = sec_list

    stock: Stock = receive_input(pieces_list, dic_incopat, sheet, space)
    return ret_output(stock=stock, skip=skip, function_type=funct_type, iterations_count=iterations_count, population_size=population_size)
