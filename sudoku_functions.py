import random
import sys
import copy


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