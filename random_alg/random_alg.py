import random
import time

from .heuristics.definitions import Piece, Stock, Subject

from .heuristics.heuristic_1 import heuristic_1 as h1
from .heuristics.heuristic_3 import h3_width_constructor as h2
from .heuristics.heuristic_4 import h4_length_constructor as h3

from .optimization_meths import *
from .utils import *


class Random_A:
    def __init__(self, stock: Stock, skip: bool, function_type: int, iterations_count: int, population_size: int) -> None:
        self.time_start = time.time()

        # Inputs
        self.skip = skip
        self.stock: Stock = stock
        # self.heuristic_list = [h1, h2, h3]
        self.heuristic_list = [h1]
        self.obj_func_type: int = function_type
        # the max number of iterations to do
        self.iterations_count: int = iterations_count

        # About pieces
        self.diferent_pieces_list: list[tuple[Piece, int]] = get_diferent_pieces(
            self.stock)
        self.diferent_pieces_list_len:int=len(self.diferent_pieces_list)    

        self.all_pieces: list[Piece] = extend_pieces(
            self.diferent_pieces_list)
        self.pieces_id_dict: dict = {}
        for i in range(len(stock.pieces)):
            self.pieces_id_dict[stock.pieces[i][0].id] = i

        self.subjects_len: int = get_max_pieces_number(self.stock)

        self.population_size: int = 2*len(self.stock.pieces)


    def heuristic_selection(self):
        '''
            Select the way to select a new heuristic to apply to the new subject
            Parameters:
                -type:
                    -1 Select a random heuristic
            Return:
                -a heuristic that is a function        
        '''
        l = len(self.heuristic_list)-1
        rand = random.randint(0, l)
        return self.heuristic_list[rand], rand+1

    def built_population(self):
        '''
            Generates a random population of size population_size with every
            list of pieces random.
            Return:
                -New population: list[Subject]
        '''

        res: list[Subject | None] = [None]*(self.population_size-self.diferent_pieces_list_len)

        for sub_i in range(self.population_size-self.diferent_pieces_list_len):
            new_chromosome_pieces: list[Piece | None] = [
                None]*self.subjects_len

            for gene_i in range(self.subjects_len):
                rand = random.randint(0, len(self.all_pieces)-1)
                to_add = self.all_pieces[rand]
                new_chromosome_pieces[gene_i] = to_add

            heuristic, heuristic_number = self.heuristic_selection()
            new_subject = Subject(stock=self.stock, dic=self.pieces_id_dict, pieces=new_chromosome_pieces,
                                  heuristic_number=heuristic_number, heuristic=heuristic)
            res[sub_i] = new_subject


        for i in range(self.diferent_pieces_list_len):
            new_chromosome_pieces: list[Piece] = [self.diferent_pieces_list[i][0]]
            remain_size: int = self.subjects_len

            while remain_size > 0:
                remain_size -= 1
                rand = random.randint(0, len(self.all_pieces)-1)
                to_add = self.all_pieces[rand]
                new_chromosome_pieces.append(to_add)

            heuristic, heuristic_number = self.heuristic_selection()
            new_subject = Subject(stock=self.stock, dic=self.pieces_id_dict, pieces=new_chromosome_pieces,
                                  heuristic_number=heuristic_number, heuristic=heuristic, b=self.skip)
            res.append(new_subject)

        return res

    def run(self):
        # Related with popultion

        best_sol: list[Subject] = self.built_population()
        _, best_score, best_sol, _, best_counter = optimization_using_lingrog(
            best_sol, self.stock, self.obj_func_type)

        iteration_count: int = 0

        # Based in the number of iteration, try with others stops
        while iteration_count < self.iterations_count:

            new_population: list[Subject] = self.built_population()
            solution_found, score, current_sol, _, vars_quantity = optimization_using_lingrog(
                new_population, self.stock, self.obj_func_type)

            if solution_found:
                if score < best_score:
                    best_score = score
                    best_sol = current_sol
                    best_counter = vars_quantity
                iteration_count += 1

        time_final = time.time()-self.time_start
        minutes, seconds = divmod(time_final, 60)

        return best_score, best_sol, best_counter, f'{round(minutes)}m {round(seconds)}s'
