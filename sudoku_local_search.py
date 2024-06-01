import random
import sys
import copy

from sudoku import Sudoku
from icecream import ic

from timing import timing_decorator



random.seed(42)

MAX_ITER = 1000000
MAX_RESTART = 10


# @timing_decorator
def gen_table(board: list[int]) -> list[int]:
    valid_values = []
    for i in range(1, 10):
        count = 0
        for row in board:
            for cell in row:
                if cell == i:
                    count += 1
        valid_values +=  [i] * (9 - count)
    random.shuffle(valid_values)

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                cell = random.randint(1, 9)
                board[x][y] = valid_values[0]
                valid_values.remove(valid_values[0])

    return board

def get_blanks(board: list[int]) -> list[tuple[int, int]]:
    blanks = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                blanks += [(i, j)]
    return blanks

def calculate_blank_cell_fillers(blanks: list[tuple[int, int]], board: list[int]) -> list[list[list[bool]]]:
    valid_fillers = [[[True for _ in range(9)] for _ in range(9)] for _ in range(9)]
    for row, col in blanks:
        for i in range(9):
            same_row = board[row][i]
            same_col = board[i][col]
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
                cell = board[grid_row_start +
                                    y_offset][grid_col_start + x_offset]
                if cell:
                    valid_fillers[row][col][cell - 1] = False
    return valid_fillers

def count_unique(board: list[int]) -> bool:
    for i in range(1, 10):
        count = 0
        for row in board:
            for cell in row:
                if cell == i:
                    count += 1
        if count != 9:
            return False
    
    return True

@timing_decorator
def calc_fitness(board: list[int], i: int, j: int):
    def row_rule(board: list[int], i: int, j: int):
        row_collisions_counter = -1
        el_to_check = board[i][j]

        for el in board[i]:
            if el == el_to_check:
                row_collisions_counter += 1

        return row_collisions_counter
    
    def col_rule(board: list[int], i: int, j: int):
        col_collisions_counter = -1
        el_to_check = board[i][j]

        for el in board[:][j]:
            if el == el_to_check:
                col_collisions_counter += 1

        return col_collisions_counter
    
    def square_rule(board: list[int], i: int, j: int):
        square_collisions_counter = -1
        el_to_check = board[i][j]

        sq_i = i // 3
        sq_y = y // 3

        sq = board[sq_i: sq_i + 3][sq_y: sq_y + 3]

        for row in sq:
            for el in row:
                if el == el_to_check:
                        square_collisions_counter += 1

        return square_collisions_counter

    fitness = 0

    for i, row in enumerate(board):
        for y, _ in enumerate(row):
            fitness += row_rule(board, i, y)
            fitness += col_rule(board, i, y)
            fitness += square_rule(board, i, y)

    # All collisions will be counted twice.
    return fitness / 2

def swap_cells(board: list[int], first: tuple[int, int], second: tuple[int, int])-> list[int]:
    new_board = copy.deepcopy(board)
    new_board[first[0]][first[1]] = board[second[0]][second[1]]
    new_board[second[0]][second[1]] = board[first[0]][first[1]]
    return new_board

def find_cell_to_swap(board: list[list[int]], cell: tuple[int, int], fitness: int, blanks: list[tuple[int, int]])-> list[tuple[int, int], int]:
    best_idx = copy.deepcopy(cell)
    best_value = board[cell[0]][cell[1]]
    for blank in blanks:
        # TODO Проходя по всем пустым ячейкам, для каждой определить, можно ли поменяться с ней.
        # TODO Если так, то вычислить для неё целевую функцию и сравнить с лучшей.
        # TODO Вернуть лучшую целевую функцию и координаты ячейки с лучшей заменой.  
        pass

class Puzzle:
    """A class that represents sudoku."""

    def __init__(self, board: list[int]) -> None:
        """Initialization of a sudoku object."""
        self.board = board
        self.blanks = self._get_blanks()
        self.blank_fillers = self._calculate_blank_cell_fillers()

    def _get_blanks(self) -> list[tuple[int, int]]:
        blanks = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    blanks += [(i, j)]
        return blanks
    
    def _calculate_blank_cell_fillers(self) -> list[list[list[bool]]]:
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

    def row_rule(self, i: int, j: int)-> int:
        row_collisions_counter = -1
        el_to_check = self.board[i][j]

        for el in self.board[i]:
            if el == el_to_check:
                row_collisions_counter += 1

        return row_collisions_counter
    
    def col_rule(self, i: int, j: int):
        col_collisions_counter = -1
        el_to_check = self.board[i][j]

        for el in self.board[:][j]:
            if el == el_to_check:
                col_collisions_counter += 1

        return col_collisions_counter
    
    def square_rule(self, i: int, j: int):
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
    def _calc_fitness(self, i: int, j: int):
        fitness = 0
        for i, row in enumerate(self.board):
            for y, _ in enumerate(row):
                fitness += self.row_rule(i, y)
                fitness += self.col_rule(i, y)
                fitness += self.square_rule(i, y)

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

    blanks = get_blanks(board)
    blank_count = len(blanks)
    are_blanks_filled = [False for _ in range(blank_count)]
    blank_fillers = calculate_blank_cell_fillers(blanks, board)


    ic.disable()
    ic(blanks)
    ic(blank_fillers)
    ic(len(blank_fillers) * len(blank_fillers[0]) * len(blank_fillers[0][0]))


    filled_board = gen_table(board)
    ic(count_unique(filled_board))
    my_puzzle = Sudoku(3, 3, board=filled_board)

    my_puzzle.show_full()

    ic.disable()
    fitness = calc_fitness(filled_board, 0, 0)
    ic(fitness)


    while fitness > 0 and not no_solution:
        cell_value = filled_board[cell[0]][cell[1]]
        for cell in blanks:
            swap, new_fitness = find_cell_to_swap(filled_board, cell, fitness, blanks)
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