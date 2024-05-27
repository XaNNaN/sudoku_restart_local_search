import random

from sudoku import Sudoku
from icecream import ic

random.seed(42)

MAX_ITER = 1000000
MAX_RESTART = 10

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
    

if __name__ == "__main__":

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
    puzzle.solve().show_full()

    blanks = get_blanks(board)
    blank_count = len(blanks)
    are_blanks_filled = [False for _ in range(blank_count)]
    blank_fillers = calculate_blank_cell_fillers(blanks, board)

    ic(blank_fillers)
    ic(len(blank_fillers) * len(blank_fillers[0]) * len(blank_fillers[0][0]))


    filled_board = gen_table(board)
    ic(count_unique(filled_board))
    my_puzzle = Sudoku(3, 3, board=filled_board)

    my_puzzle.show_full()