from .definitions import Piece
from .colocations import colocate, colocate_x


def times_pattern_fit(p_length: int, p_width: int, space: int, s_length: int, s_width: int):
    '''
        Given a stock and a piece, get the maxim times that can be colocated that piece
    '''

    def times_area_fit(length: int, space: int, area: int):
        v = int(area/(length+space))
        v = v+1 if (v+1)*length+v*space <= area else v
        return v

    '''
        1- Means p_length>p_width
        2- Means p_length<p_width
        3- Means p_length=p_width
    '''

    h_pos = times_area_fit(p_length, space, s_length)
    v_pos = times_area_fit(p_width, space, s_width)
    base = h_pos*v_pos

    # if can be colocated more pieces at the right
    if p_length > p_width:
        rest = s_length-(h_pos*(space+p_length))
        to_add_h = times_area_fit(p_width, space, rest)
        to_add_v = times_area_fit(p_length, space, s_width)
        to_add = to_add_h*to_add_v
        return 1, base+to_add, [h_pos, v_pos, to_add_h, to_add_v]

    # if can be colocated more pieces at the top
    elif p_length < p_width:
        rest = s_width-(v_pos*(space+p_width))
        to_add_h = times_area_fit(p_width, space, s_length)
        to_add_v = times_area_fit(p_length, space, rest)
        to_add = to_add_h*to_add_v
        return 2, base+to_add, [h_pos, v_pos, to_add_h, to_add_v]

    # if p_length=p_width
    return 3, base, [h_pos, v_pos]


def get_max_pattern(space: int, s_length: int, s_width: int, piece: Piece):
    '''
        Get the distribution of equal pieces in a pattern
    '''

    # if pieces does'nt fir i can't do anything
    if (piece.length > s_length and piece.length > s_width) or (piece.width > s_length and piece.width > s_width):
        return None, None, None

    # no rotated
    choice, times, distribution = times_pattern_fit(
        piece.length, piece.width, space, s_length, s_width)
    # rotated
    choice_r, times_r, distribution_r = times_pattern_fit(
        piece.width, piece.length, space, s_length, s_width)

    if times < times_r:
        times = times_r
        piece.rotate()
        choice = choice_r
        distribution = distribution_r

 
    # basic sub_pattern
    a, n_l, n_t = colocate(0, 0, piece, space,
                           distribution[0], distribution[1])
    
    if choice == 3 or (distribution[2] == 0 and distribution[3] == 0):
        return  a, times
    
    piece.rotate()
    # has a rigth sub_pattern
    if choice == 1:
        b, _, _ = colocate(n_l, 0, piece, space,
                           distribution[2], distribution[3])
    
    # has an upper sub_pattern
    else:
        b, _, _ = colocate(0, n_t, piece, space,
                           distribution[2], distribution[3])
    
    return a+b, times
