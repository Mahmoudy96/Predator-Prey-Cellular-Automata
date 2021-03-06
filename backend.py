'''
This is the backend. Here the board info is iterated, and data is saved.
'''

from enum import Enum
from collections import namedtuple
from copy import deepcopy
from random import uniform
import numpy as np
import pygame

class CellType(Enum):
    EMPTY = 0
    PREY = 1
    PREDATOR = 2
    KILLED = 3


PPACProbabilities = namedtuple("Probabilities", ["PreyDeathRate", "PredDeathRate", "PreyBirthRate", "PredBirthRate"])
PPACData = namedtuple("Data", ["Generation", "NumberOfPrey", "NumberOfPredators"])


class PPAC:
    '''
    Predator-Prey Cellular Automaton
    This class saves the states of the system, and iterates over them
    '''
    class Cell:
        def __init__(self, row, column, cell_type):
            self.row = row
            self.column = column
            self.cell_type = cell_type
        def __repr__(self):
            return f"{self.cell_type.value}" #(row={self.row}, col={self.column}),

    def __init__(self,board=None, n_rows = 200, n_cols = 200 , initial_predators = 120, initial_prey = 60,
                 prey_death_rate = 0.4, predator_death_rate = 0.3, predator_birth_rate = 0.7, prey_birth_rate = 0.4, visuals_on=False):
        '''
        Initialize the Predator-Prey Cellular Automaton, either with a predefined board, or with height, width and
        initial number of predators/prey
        :param board:
        :param board_width:
        :param board_height:
        :param initial_predators:
        :param initial_prey:
        :param prey_death_rate:
        :param predator_death_rate:
        :param predator_eat_rate:
        :param prey_birth_rate:
        :param visuals_on:
        '''
        if board is not None:
            self.board = board
            self.n_prey, self.n_predator = self.get_board_data()
        else:
            self.board = self.create_board(m=n_rows, n=n_cols)
            self.n_predator = initial_predators
            self.n_prey = initial_prey
            if self.n_prey+self.n_predator > len(self.board)*len(self.board[0]):
                exit()
            self.populate_board()
            #populate board
        self.n_rows = len(self.board)
        self.n_columns = len(self.board[0])
        self.probabilities = PPACProbabilities(PredDeathRate=predator_death_rate, PreyDeathRate=prey_death_rate,
                                             PredBirthRate=predator_birth_rate, PreyBirthRate=prey_birth_rate)
        self.generation = 0
        self.saved_data = [PPACData(Generation=0, NumberOfPrey=initial_prey, NumberOfPredators=initial_predators)]

        #visuals placeholders, TODO: manage this properly
        self.visuals = visuals_on
        #self.shown = False
        self.win = None #pygame window placeholder

    def populate_board(self):
        '''
        randomly populates empty board according to class parameters.
        :return:
        '''

        board_size = len(self.board[0])*len(self.board) #number of rows * number of elements in row(width*height(
        prey_left = self.n_prey
        pred_left = self.n_predator
        while (prey_left + pred_left) > 0:
            for row in self.board:
                for cell in row:
                    if cell.cell_type == CellType.EMPTY:
                        rr = uniform(0,1)
                        if rr < (prey_left) / board_size:
                            self.board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.PREY)
                            prey_left -= 1
                        rr = uniform(0,1)
                        if rr < pred_left/board_size:
                            self.board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.PREDATOR)
                            pred_left -= 1
        #print(self.board)


    def run(self):
        '''
        runs the system until "completion" (everything is dead)
        maybe not a good idea? potentially infinite loop
        :return:
        '''
        while not self.stale_board():
            self.iterate()

    def iterate(self, number_of_iterations=1):
        if self.visuals and self.win is None:
            pygame.init()
            self.win = pygame.display.set_mode((400,400))#TODO: make this better
        for i in range(number_of_iterations):
            # board is copied, since we want to check status on original board, and update them on the copied board,
            # to prevent overwriting our board with changes and reading changes as old board state
            #check if board is populated or not
            if self.visuals:
                #self.print_board()
                #self.render_board()
                self.render_board()
            if self.stale_board():

                print("Game over!")
                break

            iter_board = deepcopy(self.board)
            self.generation += 1
            #iterate according to rules, update
            for row in self.board:
                for cell in row:
                    neighbours = self.get_neighbours(cell,"Moore")
                    #print(neighbours)
                    live_prey = 0
                    live_predators = 0
                    for neighbour in neighbours:
                        if neighbour.cell_type == CellType.PREY:
                            live_prey += 1
                        if neighbour.cell_type == CellType.PREDATOR:
                            live_predators += 1
                    #We've calculated the cell's environment, now we can apply our rules


                    #Rule 1: if there are between 2-4 neighboring prey, populate cell according to prey birth rate
                    if cell.cell_type == CellType.EMPTY:
                        if live_prey > 0:
                            if live_predators == 0:
                                rr=uniform(0,1)
                                if rr <= self.probabilities.PreyBirthRate:
                                   iter_board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.PREY)
                            else:
                                rr1 = uniform(0,1)
                                rr2 = uniform(0,1)
                                if rr1 <= self.probabilities.PredBirthRate and rr2 <= self.probabilities.PreyDeathRate:
                                    iter_board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.PREDATOR)
                    #elif cell.cell_type == CellType.KILLED:
                        #rr = uniform(0,1)
                        #if rr <= self.probabilities.PredBirthRate:
                    elif cell.cell_type == CellType.PREY:
                        if live_predators >= 1:
                            rr = uniform(0,1)
                            if rr <= self.probabilities.PreyDeathRate:
                                rr = uniform(0,1)
                                if rr <= self.probabilities.PredBirthRate:
                                    iter_board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.PREDATOR)
                                else:
                                    iter_board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.EMPTY)
                    else:
                        rr = uniform(0,1)
                        if rr <= self.probabilities.PredDeathRate:
                            iter_board[cell.row][cell.column] = self.Cell(cell.row, cell.column, CellType.EMPTY)


            #at the end, update system information:
            self.board = deepcopy(iter_board)
            self.n_prey, self.n_predator = self.get_board_data()
            self.saved_data.append(PPACData(Generation=self.generation, NumberOfPrey=self.n_prey, NumberOfPredators=self.n_predator))

    def stale_board(self):
        '''
        checks if there are any predators/prey on the board
        :return:
        '''

        '''
        dead = True

        for row in self.board:
            for cell in row:
                if cell.cell_type == CellType.PREDATOR or cell.cell_type == CellType.PREY:
                    dead = False
        return dead
        '''
        if (self.n_predator == 0 and self.n_prey == 0) or self.n_prey == self.n_rows*self.n_columns:
            return True
        else:
            return False

    def get_board_data(self):
        '''
        :return: number of prey and predators respectively on the current board
        '''
        n_prey = 0
        n_predator = 0
        for row in self.board:
            for cell in row:
                if cell.cell_type == CellType.PREY:
                    n_prey += 1
                if cell.cell_type == CellType.PREDATOR:
                    n_predator += 1
        return n_prey, n_predator

    def get_neighbours(self, center_cell:Cell, neighbourhood_type="Moore"):
        '''
        get the neighbours of the cell according to Moore or Von Neumann neighbourhood
        Moore: 8 cells surrounding the cells
        Von Neumann: 4 cells directly adjacent to the cell
        TODO: add radius?
        :param center_cell:
        :param neighbourhood_type: "Moore" for Moore neighbourhood, "VN" for Von Neumann neighbourhood
        :return:
        '''
        neighbours = []
        for row in self.board:
            for cell in row:
                if cell.row == center_cell.row and cell.column == center_cell.column:
                    continue
                if neighbourhood_type == "Moore":
                    if abs(cell.row - center_cell.row) <= 1 and abs(cell.column - center_cell.column) <= 1:
                        neighbours.append(deepcopy(cell))
                elif neighbourhood_type == "VN":
                    if (abs(cell.row - center_cell.row)+abs(cell.column - center_cell.column)) == 1:
                        neighbours.append(deepcopy(cell))

        return neighbours


    def create_board(self, m, n):
        '''
        Creates an empty(populated by 0s) board(mxn matrix)
        :param m: width
        :param n: height
        :return:
        '''
        return [[self.Cell(j, i, CellType.EMPTY) for i in range(m)] for j in range(n)]
        #rows are size m lists, of which there are n.

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))
        return

    def render_board(self):
        if self.visuals is False:
            pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.visuals = False
        scale_factor_x = int(400/self.n_columns)
        scale_factor_y = int(400/self.n_rows)
        mat = np.ones((self.n_columns*scale_factor_x, self.n_rows*scale_factor_y), dtype=(int, 3)) * 255
        for row in self.board:
            for cell in row:
                cell_x = cell.column*scale_factor_x
                cell_y = cell.row*scale_factor_y
                color = (255, 255, 255)
                if cell.cell_type == CellType.PREY:
                    color = (0, 0, 255)
                elif cell.cell_type == CellType.PREDATOR:
                    color = (255, 0, 0)
                mat[cell_x:cell_x+scale_factor_x, cell_y:cell_y+scale_factor_y] = color
        surf = pygame.surfarray.make_surface(mat)
        self.win.blit(surf, (0, 0))
        pygame.display.update()
