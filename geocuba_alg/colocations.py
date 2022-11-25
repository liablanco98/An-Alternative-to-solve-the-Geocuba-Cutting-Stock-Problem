from .definitions import Piece


def colocate(start_l: int, start_w: int, piece: Piece, space: int, to_the_right: int, to_up: int):
    '''
        Given a start position and a sub_sheet, colocate a piece
        Return  the patttern, the new l pos, the new w pos
    '''

    temp_pattern: list[tuple(tuple(int, int), tuple(int, int), Piece)] = []

    if piece.rotation:
        width = piece.length
        length = piece.width
    else:
        width = piece.width
        length = piece.length

    cursor_l = start_l

    while to_up:
        copy_ttr = 0

        while copy_ttr < to_the_right:
            temp = ((cursor_l, start_w), (cursor_l+length, start_w+width), piece)
            temp_pattern.append(temp)
            cursor_l += length+space
            copy_ttr += 1

        start_w += space+width
        to_up -= 1
        cursor_l = start_l

    return temp_pattern, cursor_l, start_w


def colocate_x(start_l: int, start_w: int, piece: Piece, space: int, to_the_right: int, to_up: int, x: int):
    '''
        Given a start position and a sub_sheet, colocate a piece x times
        Return  the patttern, the new l pos, the new w pos
    '''

    temp_pattern: list[tuple(tuple(int, int), tuple(int, int), Piece)] = []

    if piece.rotation:
        width = piece.length
        length = piece.width
    else:
        width = piece.width
        length = piece.length

    cursor_l = start_l
    while to_up and x:
        copy_ttr = 0

        while copy_ttr < to_the_right and x:
            temp = ((cursor_l, start_w), (cursor_l+length, start_w+width), piece)
            temp_pattern.append(temp)
            x -= 1
            cursor_l += length+space
            copy_ttr += 1

        start_w += space+width
        to_up -= 1
        cursor_l = start_l

    return temp_pattern, cursor_l, start_w, x
