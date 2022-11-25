# from pulp import *
import scipy.optimize
from .heuristics.definitions import Piece, Stock, Subject
from operator import neg


def optimization_using_lingrog(subjects: list[Subject], stock: Stock, b: int = 1) -> tuple[bool, int, list[Subject] | None, list[Subject] | None]:
    subjects_number = len(subjects)
    obj = [0]*subjects_number
    obj1 = [1]*subjects_number
    alls = [None]*subjects_number

    for sub in range(subjects_number):
        subject = subjects[sub]
        obj[sub] = subject.waste
        alls[sub] = list(map(neg, subject.all_pieces_considered))

    contrains = list(map(list, zip(*alls)))
    integrity = [1]*subjects_number
    bounds = [(0, None)]*subjects_number

    b_vector = stock.neg_demand_list
    to_compare = stock.demand_list

    # minimize the number of sheets
    if b == 1:
        res = scipy.optimize.linprog(
            obj1, A_ub=contrains, b_ub=b_vector, bounds=bounds, integrality=integrity)

        if not (res.success):
            # print("No found")
            return False, -1, None, None, None

        values: list[int] = []
        best_subj: list[Subject] = []
        other_sub: list[Subject] = []
        for pos in range(subjects_number):
            val = round(res.x[pos])
            if val > 0:
                best_subj.append(subjects[pos])
                values.append(val)
            else:
                other_sub.append(subjects[pos])

        alls = [0]*len(stock.demand_list)
        to_delete = 0
        for pos in range(len(best_subj)):
            all_considered = best_subj[pos].all_pieces_considered
            val = values[pos]
            to_delete += val*best_subj[pos].waste
            for alls_pos in range(len(alls)):
                alls[alls_pos] += val*all_considered[alls_pos]

        to_increase = 0
        for index in range(len(to_compare)):
            dif = alls[index]-to_compare[index]
            if dif < 0:
                print('Error')
            to_increase += dif*stock.pieces_area[index]

        obj_result = to_delete+to_increase

        return True, obj_result, best_subj, other_sub, values

    res = scipy.optimize.linprog(
        obj, A_ub=contrains, b_ub=b_vector, bounds=bounds, integrality=integrity)

    if not (res.success):
        return False, -1, None, None, None

    values: list[int] = []
    best_subj: list[Subject] = []
    other_sub: list[Subject] = []
    for pos in range(subjects_number):
        val = round(res.x[pos])
        if val > 0:
            best_subj.append(subjects[pos])
            values.append(val)
        else:
            other_sub.append(subjects[pos])

    # minimize the waste and all pieces thata are not needed ar considered waste
    if b == 2:
        alls = [0]*len(stock.demand_list)
        for pos in range(len(best_subj)):
            all_considered = best_subj[pos].all_pieces_considered
            val = values[pos]
            for alls_pos in range(len(alls)):
                alls[alls_pos] += val*all_considered[alls_pos]

        to_increase = 0

        for index in range(len(to_compare)):
            dif = alls[index]-to_compare[index]
            if dif < 0:
                print('Error')
            to_increase += dif*stock.pieces_area[index]

        min_optimized = round(res.fun)
        obj_result = min_optimized+to_increase

    # only consider waste
    else:
        obj_result = round(res.fun)

    return True, obj_result, best_subj, other_sub, values
