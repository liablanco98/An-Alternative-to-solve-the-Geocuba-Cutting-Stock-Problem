from .definitions import Piece, Stock
from .utils import *
from .cut_used_sheet import *
import time


def FFD_CUT_2D(stock: Stock):
    '''
        Sort the pieces for area in not ascending order
    '''

    def area(v: tuple[Piece, int]) -> int:
        return v[0].area()

    def sort_by_area(pieces) -> list[(Piece, int)]:
        pieces: list[(Piece, int)] = stock.pieces
        pieces.sort(key=area, reverse=True)
        return pieces

    sorted = sort_by_area(stock)

    '''
        Extending the pieces
    '''
    def extend_pieces_list(pieces: list[tuple[Piece, int]]) -> list[Piece]:
        result: list[Piece] = []
        for piece in pieces:
            p = [piece[0]]
            demand = piece[1]
            temp = p*demand
            result.extend(temp)
        return result

    items: list[Piece] = extend_pieces_list(sorted)

    m: int = len(items)
    h_i: list[dict[int, tuple[tuple[int, int], tuple[int, int]]]] = []
    v_i: list[dict[int, tuple[tuple[int, int], tuple[int, int]]]] = []
    f_i: list[dict[int, tuple[tuple[int, int], tuple[int, int]]]] = []
    b_i: list[list[tuple[tuple[int, int], tuple[int, int], Piece]]] = []
    dif_pieces: list[list[set()]] = []
    n = 0

    '''
        Demand
    '''
    for item_pos in range(m):
        '''
            Colocate item 
        '''
        item = items[item_pos]
        i = -1
        '''
            Check if it fits in a sheet
        '''
        for min_j in range(n):

            # Colors restriction
            dif = dif_pieces[min_j][0]
            is_disjoin = dif.isdisjoint(item.incompatible)
            if not is_disjoin:
                continue

            if fits_in(item, stock.space, h_i[min_j]) or fits_in(item, stock.space, v_i[min_j]) or fits_in(item, stock.space, f_i[min_j]):
                i = min_j
                break

        '''
            If a new sheet is needed
        '''
        if i == -1:
            h_n, v_n, b_n = cut_new_sheet(
                piece=item, stock_l=stock.length, stock_w=stock.width, space=stock.space)
            h_i.append({0: h_n})
            v_i.append({0: v_n})
            f_i.append({0: None})
            b_i.append([b_n])
            dif_pieces.append([{item.id}])
            n += 1

            '''
                Else cut an used sheet
            '''
        else:
            b_n = cut_used_sheet(piece_num=item_pos, piece=item, space=stock.space,
                                 h_sheet=h_i[i], v_sheet=v_i[i], f_sheet=f_i[i])
            curr = dif_pieces[i][0]
            curr.add(item.id)
            b_i[i].append(b_n)

    total_area = stock.stock_area*n
    areas = [pice_c.area_with_space(stock.space) for pice_c, _ in stock.pieces]
    demand = [d for _, d in stock.pieces]
    ar = 0
    for i in range(len(areas)):
        ar += areas[i]*demand[i]

    waste = total_area-ar

    return waste, b_i


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


def ret_output(stock: Stock):
    time_start = time.time()
    waste, patt = FFD_CUT_2D(stock)
    time_final = time.time()-time_start
    minutes, seconds = divmod(time_final, 60)
    time_text = f'{round(minutes)}m {round(seconds)}s'
    return waste, patt, time_text


def main(pieces_list: list[tuple[tuple[int, int, int], int]], sheet: tuple[int, int] = (700, 500), space: int = 0, incompatible: list[tuple[int, int]] = []):
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
        dic_incopat[first] = first_list

        sec_list.add(first)
        dic_incopat[sec] = sec_list

    stock: Stock = receive_input(pieces_list, dic_incopat, sheet, space)
    return ret_output(stock=stock)
