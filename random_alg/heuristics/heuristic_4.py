from .definitions import Stock, Piece, Sub_Sheet
import sys


def closest_width(sheets: list[Sub_Sheet], piece: Piece) -> tuple[Sub_Sheet, Sub_Sheet, Sub_Sheet]:
    '''
        Return the sheet with closest width
        Parameters:
            -sheets: list of subsheets already builded
            -piece: piece to find closest subsheet
        Return:
            -closest_sheet_smaller: subsheet with closeset dimentions but with width < piece.width
            -closest_sheet_bigger: subsheet with closeset dimentions but with with width >= piece.width
            -closest: the smaller between the smaller and the bigger
    '''
    closest_sheet_smaller: Sub_Sheet | None = None
    closest_sheet_bigger: Sub_Sheet | None = None
    closest_width_smaller: int = sys.maxsize
    closest_width_bigger: int = sys.maxsize

    for sheet in sheets:
        if not sheet.fit_piece_rigth(piece):
            continue

        closest = sheet.left_width-piece.width
        abs_closest = abs(closest)

        if abs_closest < closest_width_smaller and closest < 0:
            closest_sheet_smaller = sheet
            closest_width_smaller = abs_closest
        elif abs_closest < closest_width_bigger and closest >= 0:
            closest_sheet_bigger = sheet
            closest_width_bigger = abs_closest

    closest: Sub_Sheet | None = closest_sheet_bigger if closest_width_bigger <= closest_width_smaller else closest_sheet_smaller

    return closest_sheet_bigger, closest_sheet_smaller, closest


def fits(piece: Piece, sheets: list[Sub_Sheet], space: int, stock_length: int, left_width: int,  current_width_pos: int) -> tuple[bool, int, int]:
    '''
        Calculate if a piece fits in a pattern
        Parameters:
            -piece: Piece to see if can be colocated
            -sheets: list of subsheets already builded
            -space: int related to the spaces that needs to be between two pieces
            -stock_length: int length of the stock
            -left_width: int that is stock.width- each subsheet_width
            -current_width_pos:int position of the left_width
        Return:
            -Bool: if the piece can or not be colocated
            -Int: represents the left_width value updated
            -Int: represents the current_width_pos value updated
    '''
    sheet_bigger, sheet_smaller, sheet_closest = closest_width(sheets, piece)

    # Means there is a sheet where is fits at the rigth
    if sheet_closest:

        # If needs to be increased the width
        if sheet_smaller and sheet_closest == sheet_smaller:
            dif = piece.width-sheet_smaller.left_width

            if dif > left_width:
                # If does'nt fit and cannot be colocated in any other
                if sheet_bigger is None:
                    return False, left_width, current_width_pos

                # Else colocated in the closest bigger
                else:
                    sheet_closest = sheet_bigger

            # else can be abapted the sheet (incresead the current width)
            else:
                left_width -= dif
                sheet_closest.increase_width(dif)

        # If not change needit
        sheet_closest.colocate_rigth_piece(piece)
        return True, left_width, current_width_pos

    # else check if a new sub_sheet can be added
    if left_width >= piece.width+space:
        sheet = Sub_Sheet(length=stock_length, width=piece.width, space=space)
        sheet.colocate_rigth_piece(piece)
        sheets.append(sheet)

        # Updating values
        left_width -= piece.width+space
        current_width_pos += piece.width+space
        return True, left_width, current_width_pos

    # else means that a new sheet can not be added
    return False, left_width, current_width_pos


def h4_length_constructor(stock: Stock, pieces: list[Piece],skip:bool=False) -> tuple[int, list[tuple[tuple[int, int], tuple[int, int], Piece]], dict[Piece, int]]:
    '''
        It builds the pattern constructing subsheets (fits)
        - If there is not subsheet construct one with the width of the first piece, and put that piece at the left
        - If there are subsheets:
            -For each that can be colocated (the remained space of the sheet is >= piece.length +space) find the one with
            closest width
                -if closest width is smaller then the piece width:
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

    # Starting...
    sheets: list[Sub_Sheet] = []
    left_width: int = stock.width
    current_width_pos: int = 0
    dif_pieces: set[int] = set()

    # Building the sheets
    for piece in pieces:

        is_disjoin = dif_pieces.isdisjoint(piece.incompatible)
        if not is_disjoin:
            if not skip:
                break
            continue

        fits_piece, left_width, current_width_pos = fits(
            piece=piece, sheets=sheets, space=stock.space, stock_length=stock.length, left_width=left_width, current_width_pos=current_width_pos)

        if not fits_piece:
            if not skip:
                break
            continue

        else:
            dif_pieces.add(piece.id)

    # Getting the answer
    pattern: list[tuple[tuple[int, int], tuple[int, int], Piece]] = []
    occupied_area: int = 0
    dic_pieces: dict[Piece, int] = {}

    current_width = 0
    for sheet in sheets:
        for start_l, last_l, piece in sheet.items:
            i = ((start_l, current_width),
                 (last_l, current_width+piece.width), piece)
            pattern.append(i)
            occupied_area += piece.area_with_space(stock.space)
            value = dic_pieces.get(piece, 0)+1
            dic_pieces[piece] = value
        current_width += sheet.current_width_pos+stock.space

    # pieces_list = list(dic_pieces.items())
    waste = stock.stock_area-occupied_area

    # print(f'Pattern Using H4\n')
    # for x in pattern:
    #     print(f"{x}\n")
    # print(f'waste {waste}')

    # return waste, pattern, pieces_list
    return waste, pattern, dic_pieces


# p1 = Piece(1, 220, 320)
# p2 = Piece(2, 240, 300)
# p3 = Piece(3, 200, 340)
# p4 = Piece(4, 225, 150)
# p5 = Piece(5, 527, 20)
# p6 = Piece(6, 205, 100)
# s = Stock(space=2)
# r = h4_length_constructor(s, [p1, p2, p3, p4, p5,p6], True)
