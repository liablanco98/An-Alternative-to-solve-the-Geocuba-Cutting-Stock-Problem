from .definitions import Piece, Stock
from .utils import get_max_pattern
import time


def simple_colocation_algorithm(stock: Stock, func_type):
    '''
    Colocate in sheets only equal pieces 
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

    # list of positions of pieces and number of pieces
    patterns_list: list[tuple[tuple[list[tuple[tuple[int, int],
                                         tuple[int, int], Piece], int], int]]] = []

    for piece, demand in stock.pieces:
        pattern, size = get_max_pattern(
            space=stock.space, s_length=stock.length, s_width=stock.width, piece=piece)

        times = int(demand/size)
        times += 1 if demand % size > 0 else 0
        patterns_list.append(((pattern, size), times))

    '''
        After calculated the patterns obteined, get:
        each pattern waste
        pieces used and repetitions in each pattern
        total waste=sum each pattern waste
    '''
    patterns: list[tuple[tuple[int, list[tuple[tuple[int, int],
                                               tuple[int, int], int]], list[tuple[int, int]]], int]] = []

    demand: dict[int, int] = {}
    for p, d in stock.pieces:
        demand[p.id] = d

    waste = 0
    for pattern, count in patterns_list:
        patt, pieces_colocated = pattern

        # All pieces are equal son the area is the same
        _, _, p = patt[0]
        piece_area: int = p.area_with_space(stock.space)

        second: list[tuple[tuple[int, int], tuple[int, int], int]] = list(
            map(lambda x: (x[0], x[1], x[2].id), patt))
        occupied: int = piece_area*pieces_colocated
        curr_waste = stock.stock_area-occupied

        patterns.append(
            ((curr_waste, second, [p.id, pieces_colocated]), count))

        if func_type == 1:
            # fits=
            total_area = count*stock.stock_area
            piece_demand = demand[p.id]
            to_rest = piece_area*piece_demand
            # sobr=piece_demand%pieces_colocated
            # if sobr>0:
            #     t=(piece_area*sobr)
            this_waste = total_area-to_rest

        else:
            this_waste = curr_waste*count
        waste += this_waste
    return waste, patterns


def receive_input(pieces_list: list[tuple[tuple[int, int, int], int]], dict_incompatible: dict[int, set], sheet: tuple[int, int] = (700, 500), space: int = 0) -> Stock:
    '''
        Parameters:
            - pieces: list of tuple ((piece id, length, piece width),piece demand)
            - dict_incompatible: a dictionary[int,set] that gives the set of pieces that cannot be colocated next to the piece id
            - sheet: tuple (sheet length, sheet width)
            - space: an int with the space that most be left between sheets
    '''
    # Buiding the pieces_list
    pieces: list[tuple[Piece, int]] = list()
    for val, demand in pieces_list:
        id = val[0]
        length = val[1]
        width = val[2]
        incompatible = dict_incompatible.get(id, set())
        pieces.append((Piece(id, length, width, incompatible), demand))

    return Stock(length=sheet[0], width=sheet[1], pieces=pieces, space=space)


def ret_output(stock: Stock, func_type):
    time_start = time.time()
    waste, patt = simple_colocation_algorithm(stock, func_type)
    time_final = time.time()-time_start
    minutes, seconds = divmod(time_final, 60)
    time_text = f'{round(minutes)}m {round(seconds)}s'
    return waste, patt, time_text


def main(pieces_list: list[tuple[tuple[int, int, int], int]], sheet: tuple[int, int] = (700, 500), space: int = 0, incompatible: list[tuple[int, int]] = [], funct_type: int = 1):
    '''
        Receives the input and returns the results of applying a genetic solver method for cutting material problem
        Parameters:
            - pieces_list: a list of ((piece id, piece length, piece width), piece demand)
            - sheet: (sheet length, sheet width)
            - space: the space that needs to be maintained between two consecutive pieces
            - incompatible: a list of tuples representing the identifiers of pieces that cannot be placed on the same sheet
            - func_type: is an int. When is 1 all pieces over the demand anre waste, when is 2 the waste is the space without pieces
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
        sec_list.add(first)

    stock: Stock = receive_input(pieces_list, dic_incopat, sheet, space)
    return ret_output(stock=stock, func_type=funct_type)
