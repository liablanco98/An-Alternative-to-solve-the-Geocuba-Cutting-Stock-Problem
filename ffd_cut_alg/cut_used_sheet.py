
from .definitions import Piece
from .utils import *


def cut_used_sheet(piece_num: int, piece: Piece, space: int, h_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]]], v_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]]], f_sheet: dict[int, tuple[tuple[int, int], tuple[int, int]]]):
    def get_max(dict_input: dict[int, tuple[tuple[int, int], tuple[int, int]]], sheet_pos, rot,t_m_i, t_m_key, t_m_max_value, t_m_tuple):
        for k, v in dict_input.items():
            if v is None:
                continue
            start, last = v
            l = last[0]-start[0]
            w = last[1]-start[1]
            normal = (l//(piece.length+space)*(w//(piece.width+space)))
            rotated = (l//(piece.width+space)*(w//(piece.length+space)))

            if rotated > normal:
                rot_c=True
                temp_max = rotated
            else:
                rot_c =False
                temp_max = normal

            if temp_max > t_m_max_value:
                rot=rot_c
                t_m_max_value = temp_max
                t_m_key = k
                t_m_i = sheet_pos
                t_m_tuple = v
        return rot,t_m_i, t_m_key, t_m_max_value, t_m_tuple

    rot,max_i, max_pos, max_value, sheet_selected = get_max(
        h_sheet, 1,False, 0, -1, 0, None)
    rot,max_i, max_pos, max_value, sheet_selected = get_max(
        v_sheet, 2,rot, max_i, max_pos, max_value, sheet_selected)
    rot,max_i, max_pos, max_value, sheet_selected = get_max(
        f_sheet, 3, rot,max_i, max_pos, max_value, sheet_selected)

    ((p1, p2), (p3, p4)) = sheet_selected

    if rot:
        piece_l = piece.width
        piece_w = piece.length
    else:
        piece_l = piece.length
        piece_w = piece.width

    # if the item must be colocated in the h_i_item
    if max_i == 1:
        del h_sheet[max_pos]
        if v_sheet[max_pos]:
            temp = v_sheet[max_pos]
            new_f = (temp[0], (p3, p2))
            f_sheet[piece_num] = new_f
        del v_sheet[max_pos]

    # if the item must be colocated in the v_i_item
    elif max_i == 2:
        del v_sheet[max_pos]
        if h_sheet[max_pos]:
            temp = h_sheet[max_pos]
            new_f = (temp[0], (p1, p4))
            f_sheet[piece_num] = new_f
        del h_sheet[max_pos]

    else:
        del f_sheet[max_pos]

    b_temp = ((p1, p2), (p1+piece_l, p2+piece_w), piece)
    if (to_add := p2+piece_w+space) < p4:
        h_temp = ((p1, to_add), (p3, p4))
        h_sheet[piece_num] = h_temp
    else:
        h_sheet[piece_num] = None
    if (to_add := p1+piece_l+space) < p3:
        v_temp = ((to_add, p2), (p3, p4))
        v_sheet[piece_num] = v_temp
    else:
        v_sheet[piece_num] = None
    return b_temp
