import random
import sys
import copy


from sudoku import Sudoku
from icecream import ic


import sudoku_functions as funcs
from timing import timing_decorator



random.seed(42)

MAX_ITER = 1000000
MAX_RESTART = 10

class Puzzle:
    """A class that represents sudoku."""

    def __init__(self, board: list[int]) -> None:
        """
        Initialization of a sudoku object.

        :param board: Sudoku 3x3.
        :type board: list[int]
        """
        self.board = board
        self.blanks = self._get_blanks()
        self.blank_fillers = self._calculate_blank_cell_fillers()

    def _get_blanks(self) -> list[tuple[int, int]]:
        """
        Method to find cells whose values can be changed.
        
        :return: List with indexes of found cells.
        :rtype: list[tuple[int, int]]
        """
        blanks = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    blanks += [(i, j)]
        return blanks
    
    def _calculate_blank_cell_fillers(self) -> list[list[list[bool]]]:
        """
        Method for determining available values in empty cells.

        :return: Boolean map of available values for each cell. But only applies to empty cells.
        :rtype: list[list[list[bool]]]
        """
        valid_fillers = [[[True for _ in range(9)] for _ in range(9)] for _ in range(9)]
        for row, col in self.blanks:
            for i in range(9):
                same_row = self.board[row][i]
                same_col = self.board[i][col]
                if same_row and i != col:
                    valid_fillers[row][col][same_row - 1] = False
                if same_col and i != row:
                    valid_fillers[row][col][same_col - 1] = False
            grid_row, grid_col = row // 3, col // 3
            grid_row_start = grid_row * 3
            grid_col_start = grid_col * 3
            for y_offset in range(3):
                for x_offset in range(3):
                    if grid_row_start + y_offset == row and grid_col_start + x_offset == col:
                        continue
                    cell = self.board[grid_row_start +
                                        y_offset][grid_col_start + x_offset]
                    if cell:
                        valid_fillers[row][col][cell - 1] = False
        return valid_fillers

    def _row_rule(self, i: int, j: int)-> int:
        """
        Method of counting the number of identical values in a row. For cell with specified indices.

        :param i: Row index.
        :type i: int
        :param j: Column index.
        :type j: int

        :return: Number of identical values in a row.
        :rtype int
        """
        row_collisions_counter = -1
        el_to_check = self.board[i][j]

        for el in self.board[i]:
            if el == el_to_check:
                row_collisions_counter += 1

        return row_collisions_counter
    
    def _col_rule(self, i: int, j: int):
        """
        Method of counting the number of identical values in a column. For cell with specified indices.

        :param i: Row index.
        :type i: int
        :param j: Column index.
        :type j: int

        :return: Number of identical values in a column.
        :rtype int
        """        
        col_collisions_counter = -1
        el_to_check = self.board[i][j]

        for el in self.board[:][j]:
            if el == el_to_check:
                col_collisions_counter += 1

        return col_collisions_counter
    
    def _square_rule(self, i: int, j: int):
        """
        Method of counting the number of identical values in a square, which contains cell with specified indices.

        :param i: Row index.
        :type i: int
        :param j: Column index.
        :type j: int

        :return: Number of identical values in a square.
        :rtype int
        """
        square_collisions_counter = -1
        el_to_check = self.board[i][j]

        sq_i = i // 3
        sq_j = j // 3

        sq = self.board[sq_i: sq_i + 3][sq_j: sq_j + 3]

        for row in sq:
            for el in row:
                if el == el_to_check:
                        square_collisions_counter += 1

        return square_collisions_counter

    @timing_decorator
    def calc_fitness(self)-> int:
        """
        Method to calculate goal function. Number of conflicts in this case.
        """
        fitness = 0
        for i, row in enumerate(self.board):
            for y, _ in enumerate(row):
                fitness += self._row_rule(i, y)
                fitness += self._col_rule(i, y)
                fitness += self._square_rule(i, y)

        # All collisions will be counted twice.
        return fitness / 2

if __name__ == "__main__":
    no_solution = False
    count_iter  = 0
    board = [
        [6, 0, 0, 8, 0, 0, 0, 0, 0],
        [2, 8, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 8, 4],
        [0, 0, 1, 7, 0, 0, 0, 5, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 4, 0, 0, 0, 9, 3, 0, 0],
        [4, 7, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 4, 6],
        [0, 0, 0, 0, 0, 0, 7, 0, 9],
    ]

    puzzle = Sudoku(3, 3, board=board)
    puzzle.show_full()
    # puzzle.solve().show_full()

    blanks = funcs.get_blanks(board)
    blank_count = len(blanks)
    are_blanks_filled = [False for _ in range(blank_count)]
    blank_fillers = funcs.calculate_blank_cell_fillers(blanks, board)


    # ic.disable()
    ic(blanks)
    ic(blank_fillers)
    ic(len(blank_fillers) * len(blank_fillers[0]) * len(blank_fillers[0][0]))


    filled_board = funcs.gen_table(board)
    ic(funcs.count_unique(filled_board))
    my_puzzle = Sudoku(3, 3, board=filled_board)

    my_puzzle.show_full()

    ic.disable()
    fitness = funcs.calc_fitness(filled_board, 0, 0)
    ic(fitness)


    while fitness > 0 and not no_solution:
        cell_value = filled_board[cell[0]][cell[1]]
        for cell in blanks:
            swap, new_fitness = funcs.find_cell_to_swap(filled_board, cell, fitness, blanks)
            if new_fitness == fitness:
                no_solution = True

            count_iter += 1
            fitness = new_fitness
            filled_board[cell[0]][cell[1]] = filled_board[swap[0]][swap[1]]
            filled_board[swap[0]][swap[1]] = cell_value



    if no_solution:
        print("Решение не было найдено. Остановка в локальном минимуме или на плато.")
        sys.exit(0)

    print(f"Решение было найдено за {count_iter}")
    solved = Sudoku(3, 3, board=filled_board)
    solved.show_full()