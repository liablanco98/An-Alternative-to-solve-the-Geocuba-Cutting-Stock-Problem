from .definitions import Piece, Stock


def fits_in(piece: Piece, space: int, sheets: dict[int, tuple[tuple[int, int], tuple[int, int]] | None]):
    if len(sheets):
        for v in sheets.values():
            if v is None:
                continue
            start, last = v
            if piece.length in range(last[0]-start[0]-space+1) and piece.width in range(last[1]-start[1]-space+1):
                return True
    return False


def cut_used_sheet(piece_num: int, piece: Piece, space: int, h_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]] | None], v_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]] | None], f_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]] | None]):
    def get_max(dict_input: dict[int, tuple[tuple[int, int], tuple[int, int]] | None], sheet_pos, t_m_i, t_m_key, t_m_max_value, t_m_tuple):
        for k, v in dict_input.items():
            if v is None:
                continue
            start, last = v
            l = last[0]-start[0]
            w = last[1]-start[1]
            temp_max = (l//(piece.length+space))*(w//(piece.width+space))
            if temp_max > t_m_max_value:
                t_m_max_value = temp_max
                t_m_key = k
                t_m_i = sheet_pos
                t_m_tuple = v
        return t_m_i, t_m_key, t_m_max_value, t_m_tuple

    max_i, max_pos, max_value, sheet_selected = get_max(
        h_sheet, 1, 0, -1, 0, None)
    max_i, max_pos, max_value, sheet_selected = get_max(
        v_sheet, 2, max_i, max_pos, max_value, sheet_selected)
    max_i, max_pos, max_value, sheet_selected = get_max(
        f_sheet, 3, max_i, max_pos, max_value, sheet_selected)

    ((p1, p2), (p3, p4)) = sheet_selected

    # A vertical cut must be made
    if max_i == 1:
        del h_sheet[max_pos]
        if v_sheet[max_pos]:
            temp = v_sheet[max_pos]
            new_f = (temp[0], (p3, p2))
            f_sheet[piece_num] = new_f
        del v_sheet[max_pos]

    # A horizontal
    elif max_i == 2:
        del v_sheet[max_pos]
        if h_sheet[max_pos]:
            temp = h_sheet[max_pos]
            new_f = (temp[0], (p1, p4))
            f_sheet[piece_num] = new_f
        del h_sheet[max_pos]

    else:
        del f_sheet[max_pos]

    b_temp = ((p1, p2), (p1+piece.length, p2+piece.width), piece)
    if (to_add := p2+piece.width+space) < p4:
        h_temp = ((p1, to_add), (p3, p4))
        h_sheet[piece_num] = h_temp
    else:
        h_sheet[piece_num] = None
    if (to_add := p1+piece.length+space) < p3:
        v_temp = ((to_add, p2), (p3, p4))
        v_sheet[piece_num] = v_temp
    else:
        v_sheet[piece_num] = None
    return b_temp


# Using FFD 2D Cut heuristic
def heuristic_1(stock: Stock, pieces: list[Piece], skip: bool = False) -> tuple[int, list[tuple[tuple[int, int], tuple[int, int], Piece]], dict[Piece, int]]:
    '''
        It builds the pattern using FFD cutting
        - If there is not subsheet construct one width the length of the first piece, and put that piece at the top
        - If there are subsheets:
            -For each that can be colocated (the remained space of the sheet is >= piece.width +space) find the one with
            closest length
                -if closest length is smaller then the piece length:
                    -If can be increased, is increased
                    -Can not be colocated
                -Else is colocated the piece in that sheet
            -If can't be colocated in any sheet a new sheet is created if is possible, or the piece cannot be colocated

        Parameters:
        - stock: Stock with sheets size and pieces, demand list
        - pieces: list[Pieces] to be colocated
        - skip: bool (optional) if is true, when a piece can not be colocated, continues with the next one

        Return: 
        - The pattern waste 
        - The pattern resulted
        - The pieces colocated and the number of times

    '''

    first_piece: Piece = pieces[0]
    # list of finals positions
    pattern: list[tuple[tuple[int, int], tuple[int, int], Piece]] = [
        ((0, 0), (first_piece.length, first_piece.width), first_piece)]

    # list of horizontals cuts
    if first_piece.width+stock.space < stock.width:
        h_i: dict[int, tuple[tuple[int, int], tuple[int, int]] | None] = {
            0: ((0, first_piece.width+stock.space), (stock.length, stock.width))}
    else:
        h_i: dict[int, tuple[tuple[int, int],
                             tuple[int, int]] | None] = {0: None}

    # list of verticals cuts
    if first_piece.length+stock.space < stock.length:
        v_i: dict[int, tuple[tuple[int, int], tuple[int, int]] | None] = {
            0: ((first_piece.length+stock.space, 0), (stock.length, stock.width))}
    else:
        v_i: dict[int, tuple[tuple[int, int],
                             tuple[int, int]] | None] = {0: None}

    # f_i: dict[tuple[tuple[int, int], tuple[int, int]],
    #           tuple[tuple[int, int], tuple[int, int]] | None] = {0: None}

    f_i: dict[int, tuple[tuple[int, int], tuple[int, int]] | None] = {0: None}
    l = len(pieces)
    dif_pieces: set[int] = {first_piece.id}

    for piece_pos in range(1, l):
        piece = pieces[piece_pos]

        is_disjoin = dif_pieces.isdisjoint(piece.incompatible)
        if not is_disjoin:
            if not skip:
                break
            continue

        if fits_in(piece, stock.space, h_i) or fits_in(piece, stock.space, v_i) or fits_in(piece, stock.space, f_i):
            b_n = cut_used_sheet(piece_pos, piece, stock.space, h_i, v_i, f_i)
            pattern.append(b_n)
            dif_pieces.add(piece.id)

        elif skip:
            continue

        else:
            break

    # Getting the answer
    occupied_area: int = 0
    dic_pieces: dict[Piece, int] = {}

    for _, _, piece in pattern:
        occupied_area += piece.area_with_space(stock.space)
        value = dic_pieces.get(piece, 0)+1
        dic_pieces[piece] = value

    waste = stock.stock_area-occupied_area

    return waste, pattern, dic_pieces
