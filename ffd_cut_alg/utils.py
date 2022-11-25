from .definitions import Piece


# return if a piece fits in a sheet totatedo or not
def fits_in(piece: Piece, space: int, sheets: dict[tuple[tuple[int, int], tuple[int, int]]]):
    if len(sheets):
        for v in sheets.values():
            if v is None:
                continue
            start, last = v
            # sheet_l = second[0]-first[0]
            # sheet_w = second[1]-first[1]

            if piece.length in range(last[0]-start[0]-space+1) and piece.width in range(last[1]-start[1]-space+1):
                return True

            if piece.width in range(last[0]-start[0]-space+1) and piece.length in range(last[1]-start[1]-space+1):
                return True

            # normal = (sheet_l//(piece.length+space) *
            #           (sheet_w//(piece.width+space)))
            # if normal > 0:
            #     return True

            # rotated = (sheet_l//(piece.width+space) *
            #            (sheet_w//(piece.length+space)))
            # if rotated > 0:
            #     return True
    return False


'''
    h_tem is the new horizontal sheet
    v_tem is the new vertical sheet
    b_temp is the item attended in i
'''


def cut_new_sheet(piece: Piece, stock_l: int, stock_w: int, space: int):
    normal = (stock_l//(piece.length+space)*(stock_w//(piece.width+space)))
    rotated = (stock_l//(piece.width+space)*(stock_w//(piece.length+space)))

    if rotated > normal:
        piece_l = piece.width
        piece_w = piece.length
        # piece.rotate()

    else:
        piece_l = piece.length
        piece_w = piece.width

    b_temp = ((0, 0), (piece_l, piece_w), piece)

    if piece_w+space < stock_w:
        h_temp = ((0, piece_w+space), (stock_l, stock_w))
    else:
        h_temp = None

    if piece_l+space < stock_l:
        v_temp = ((piece_l+space, 0), (stock_l, stock_w))
    else:
        v_temp = None

    return h_temp, v_temp, b_temp
