from .definitions import Stock, Piece, Sub_Sheet
import sys


def closest_length(sheets: list[Sub_Sheet], piece: Piece) -> tuple[Sub_Sheet, Sub_Sheet, Sub_Sheet]:
    '''
        Return the sheets with closest length.

        Parameters:
            -sheets: list of subsheets already builded
            -piece: piece to find closest subsheet
        Return:
            -closest_sheet_smaller: subsheet with closeset dimentions but with length < piece.length
            -closest_sheet_bigger: subsheet with closeset dimentions but with length >= piece.length
            -closest: the smaller between the smaller and the bigger
    '''
    closest_sheet_smaller: Sub_Sheet | None = None
    closest_sheet_bigger: Sub_Sheet | None = None
    closest_length_smaller: int = sys.maxsize
    closest_length_bigger: int = sys.maxsize

    for sheet in sheets:
        if not sheet.fit_piece_bottom(piece):
            continue

        closest = sheet.left_length-piece.length
        abs_closest = abs(closest)
        if abs_closest < closest_length_smaller and closest < 0:
            closest_sheet_smaller = sheet
            closest_length_smaller = abs_closest
        elif abs_closest < closest_length_bigger and closest >= 0:
            closest_sheet_bigger = sheet
            closest_length_bigger = abs_closest

    closest: Sub_Sheet | None = closest_sheet_bigger if closest_length_bigger <= closest_length_smaller else closest_sheet_smaller

    return closest_sheet_bigger, closest_sheet_smaller, closest


def fits(piece: Piece, sheets: list[Sub_Sheet], space: int,  stock_width: int, left_length: int, current_length_pos: int) -> tuple[bool, int, int]:
    '''
        Calculate if a piece fits in a pattern
        Parameters:
            -piece: Piece to see if can be colocated
            -sheets: list of subsheets already builded
            -space: int related to the spaces that needs to be between two pieces
            -stock_width: int width of the stock
            -left_length: int that is stock.length- each subsheet_length
            -current_length_pos:int position of the left_length
        Return:
            -Bool: if the piece can or not be colocated
            -Int: represents the left_length value updated
            -Int: represents the current_length_pos value updated
    '''
    sheet_bigger, sheet_smaller, sheet_closest = closest_length(sheets, piece)

    # Means there is a sheet where is fits at the bottom
    if sheet_closest:

        # If needs to be increased the length
        if sheet_smaller and sheet_closest == sheet_smaller:
            dif = piece.length-sheet_smaller.left_length

            if dif > left_length:
                # If does'nt fit and cannot be colocated in any other
                if sheet_bigger is None:
                    return False, left_length, current_length_pos

                # Else colocated in the closest bigger
                else:
                    sheet_closest = sheet_bigger

            # else can be abapted the sheet (incresead the current length)
            else:
                left_length -= dif
                sheet_closest.increase_length(dif)

        # If not change needit
        sheet_closest.colocate_bottom_piece(piece)
        return True, left_length, current_length_pos

    # else check if a new sub_sheet can be added
    if left_length >= piece.length+space:
        sheet = Sub_Sheet(length=piece.length, width=stock_width, space=space)
        sheet.colocate_bottom_piece(piece)
        sheets.append(sheet)

        # Updating values
        left_length -= piece.length+space
        current_length_pos += piece.length+space
        return True, left_length, current_length_pos

    # else means that a new sheet can not be added
    return False, left_length, current_length_pos


def h2_width_constructor(stock: Stock, pieces: list[Piece], skip: bool = False) -> tuple[int, list[tuple[tuple[int, int], tuple[int, int], Piece]], dict[Piece, int]]:
    '''
        It builds the pattern constructing subsheets (fits)
        - If there is not subsheet construct one with the length of the first piece, and put that piece at the top
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

    # Starting...
    sheets: list[Sub_Sheet] = []
    left_length: int = stock.length
    current_length_pos: int = 0
    dif_pieces: set[int] = set()

    # Building the sheets
    for piece in pieces:

        is_disjoin = dif_pieces.isdisjoint(piece.incompatible)
        if not is_disjoin:
            if not skip:
                break
            continue

        fits_piece, left_length, current_length_pos = fits(
            piece=piece, sheets=sheets, space=stock.space, stock_width=stock.width, left_length=left_length, current_length_pos=current_length_pos)

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

    current_length = 0
    for sheet in sheets:
        for start_w, last_w, piece in sheet.items:
            i = ((current_length, start_w),
                 (current_length+piece.length, last_w), piece)
            pattern.append(i)
            occupied_area += piece.area_with_space(stock.space)
            value = dic_pieces.get(piece, 0)+1
            dic_pieces[piece] = value
        current_length += sheet.current_length_pos+stock.space

    waste = stock.stock_area-occupied_area

    return waste, pattern, dic_pieces
