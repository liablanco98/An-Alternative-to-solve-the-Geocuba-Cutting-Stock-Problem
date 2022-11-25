import random
import time

from .heuristics.definitions import Piece, Stock, Subject

from .heuristics.heuristic_1 import heuristic_1 as h1
from .heuristics.heuristic_2 import h2_width_constructor as h2
from .heuristics.heuristic_3 import h3_length_constructor as h3

from .optimization_meths import *
from .utils import *
from .mutations_meths import *
from .crossover_meths import *


'''
1) Randomly initialize populations p
2) Determine fitness of population
3) Until convergence repeat:
      a) Select parents from population
      b) Crossover and generate new population
      c) Perform mutation new population
      d) Calculate fitness for new population
'''


class GA:
    def __init__(self, stock: Stock, skip: bool, function_type: int,  iterations_count: int, ellitism: int , higher_matters: int, population_size: int) -> None:
        self.time_start = time.time()

        # Inputs
        self.skip = skip
        self.stock: Stock = stock
        self.heuristic_list = [h1, h2, h3]
        self.obj_func_type: int = function_type
        # the max number of iterations to do
        self.iterations_count: int = iterations_count

        # About pieces
        
        self.diferent_pieces_list: list[tuple[Piece, int]] = get_diferent_pieces(
            self.stock)
        self.diferent_pieces_list_len: int = len(self.diferent_pieces_list)

        self.all_pieces: list[Piece] = extend_pieces(
            self.diferent_pieces_list)
        self.pieces_id_dict: dict = {}
        for i in range(len(stock.pieces)):
            self.pieces_id_dict[stock.pieces[i][0].id] = i

        self.subjects_len: int = get_max_pieces_number(self.stock)*2

        self.population_size: int = population_size if (population_size != -1) and population_size >= 2 * \
            len(self.stock.pieces) else len(self.stock.pieces)*40  # See a number to start
        # if self.population_size>500:self.population_size=500    
        # if self.population_size<100:
        #     self.population_size=100    

        # Related with popultion
        self.population: list[Subject] = self.start_population()
        self.to_keep_integrity: list[Subject] = self.population[-len(self.stock.pieces):]

        # mean the % of fittest population goes to the next generation
        # self.ellitism: int = int((
            # (ellitism*self.population_size)/100)-1)
        # self.ellitism=4*len(self.stock.pieces)
         # mean the % of fittest population goes to the next generation
        self.ellitism: int = 2*self.diferent_pieces_list_len
        # self.ellitism: int = int(
            # (percent_ellitism*self.population_size)/100)  # Check
        # The rest to the population most be crossovered
        self.no_ellitism: int = self.population_size-self.ellitism

        # mean the % of fittest population Individuals will mate to produce a new subject
        percent_higher_matters_bound: int = higher_matters
        self.higher_matters_bound: int = int((
            (percent_higher_matters_bound*self.population_size)/100)-1)

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

    def start_population(self):
        '''
            Generates a random population of size population_size with every.
            Every piece is colocated at lease in one sheet
            Return:
                -New population: list[Subject]
                -A Sub population were at least each piece appears one time
        '''
        res: list[Subject] = []
        count_subjects: int = self.population_size-self.diferent_pieces_list_len

        while count_subjects:

            new_chromosome_pieces: list[Piece] = []
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

            count_subjects -= 1

        i=0
        while i<self.diferent_pieces_list_len:

            new_chromosome_pieces: list[Piece] = [self.diferent_pieces_list[i][0]]
            remain_size: int = self.subjects_len-1

            while remain_size > 0:
                remain_size -= 1
                rand = random.randint(0, len(self.all_pieces)-1)
                to_add = self.all_pieces[rand]
                new_chromosome_pieces.append(to_add)

            heuristic, heuristic_number = self.heuristic_selection()
            new_subject = Subject(stock=self.stock, dic=self.pieces_id_dict, pieces=new_chromosome_pieces,
                                  heuristic_number=heuristic_number, heuristic=heuristic, b=self.skip)
            res.append(new_subject)

            i+=1
    

        return res

    def fitness(self, best_population: list[Subject], other_pop: list[Subject]):
        '''
            Sort the population based on their waste

            Return:
                -The new population sorted 
        '''
        other_pop.sort(key=lambda x: x.waste)
        return best_population+other_pop

    def parents_selection(self):
        '''
            Get what parents to cross in order to get a new child
            Return:
                -Both parents to Merge (Subject)        
        '''
        r1 = random.randint(0, self.higher_matters_bound)
        r2 = random.randint(0, self.higher_matters_bound)
        # while r2 == r1:
        #     r2 = random.randint(0, self.higher_matters_bound)
        return self.population[r1], self.population[r2]

    def mutation(self, list_to_mutate: list[Piece], mutation_type: int = 0) -> list[Piece]:
        if mutation_type == 0:
            return swap_mutation(list_to_mutate, self.all_pieces)
        if mutation_type == 1:
            return invertion_mutation(list_to_mutate, self.all_pieces)
        return resetting_mutation(list_to_mutate, self.all_pieces)

    def crossover(self) -> list[Piece]:
        '''
            Applies the uniform crossover.
            For each gene, a parent out of the 2 mating parents is selected randomly and the gene is copied from it.

            Return:
                - list of pieces crossed

        '''
        parent1, parent2 = self.parents_selection()
        p1_list = parent1.pieces
        p2_list = parent2.pieces
        children_list = single_point_crossover(
            p1_list, p2_list, self.subjects_len, self.all_pieces)
        return children_list

    def run(self):
        '''
            Genetic Algorithm working
        '''

        # Firts best solution
        best_sol: list[Subject] = self.population
        _, best_score, best_sol, others_subj, best_counter = optimization_using_lingrog(
            self.population, self.stock, self.obj_func_type)
        self.population = self.fitness(best_sol, others_subj)

        iteration_count: int = 0
        has_improved: int = 21

        # Based in the number of iteration, try with others stops
        while iteration_count < self.iterations_count and has_improved:
            # while iteration_count < self.iterations_count:

            # Performing Elitism number of fittest subject to the next generation
            new_population: list[Subject] = self.population[:self.ellitism]

            # From self.higher_matters_bound of fittest population
            # Subjects will be crossovered

            for _ in range(self.no_ellitism):
                new_pieces = self.crossover()

                # Giving a 1/10% of probabilitie of mutate
                if random.randint(0, 19) == 9:
                    finals = self.mutation(new_pieces)
                else:
                    finals = new_pieces

                heuristic, heuristic_number = self.heuristic_selection()
                new_subject = Subject(stock=self.stock, dic=self.pieces_id_dict, pieces=finals,
                                      heuristic_number=heuristic_number, heuristic=heuristic, b=self.skip)
                new_population.append(new_subject)

            while True:
                solution_found, score, current_best_sol, current_other_subj, current_pattern_counter = optimization_using_lingrog(
                    new_population, self.stock, self.obj_func_type)

                if solution_found:
                    new_population = self.fitness(
                        current_best_sol, current_other_subj)
                    if score < best_score:
                        best_score = score
                        best_sol = current_best_sol
                        best_counter = current_pattern_counter
                        has_improved = 21
                    break

                # new_population = self.to_keep_integrity + \
                #     new_population[:-len(self.stock.pieces)]

            has_improved -= 1
            self.population = new_population
            iteration_count += 1

        time_final = time.time()-self.time_start
        minutes, seconds = divmod(time_final, 60)

        return best_score, best_sol, best_counter, f'{round(minutes)}m {round(seconds)}s'
