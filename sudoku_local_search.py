import random
import copy


from sudoku import Sudoku
from icecream import ic

random.seed(42)
class Puzzle:
    """A class that represents sudoku."""

    def __init__(self, board: list[int]) -> None:
        """
        Initialization of a sudoku object.

        :param board: Sudoku 3x3.
        :type board: list[int]
        """
        self.board = copy.deepcopy(board)
        self.init_board = copy.deepcopy(board)
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
        sq = [row[sq_j: sq_j + 3] for row in self.board[sq_i: sq_i + 3]]
        for row in sq:
            for el in row:
                if el == el_to_check:
                        square_collisions_counter += 1

        return square_collisions_counter

    # @timing_decorator
    def calc_fitness(self, board_in=None)-> int:
        """
        Method to calculate goal function. Number of conflicts in this case.
        """
        if board_in == None:
            board = self.board
        else: 
            board = copy.deepcopy(board_in)
        collisions = 0
        
        # Подсчет коллизий в строках
        for row in board:
            collisions += len(row) - len(set(row))
        
        # Подсчет коллизий в столбцах
        for col in range(len(board)):
            column_values = [board[row][col] for row in range(len(board))]
            collisions += len(column_values) - len(set(column_values))
        
        # Подсчет коллизий в квадратах 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square_values = []
                for row in range(3):
                    for col in range(3):
                        square_values.append(board[i + row][j + col])
                collisions += len(square_values) - len(set(square_values))
        
        return collisions

    def gen_table(self) -> list[int]:
        """
        A method of filling a table with values that preserves its solvability.
        """
        valid_values = []
        for i in range(1, 10):
            count = 0
            for row in self.init_board:
                for cell in row:
                    if cell == i:
                        count += 1
            valid_values +=  [i] * (9 - count)
        random.shuffle(valid_values)

        for x, row in enumerate(board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cell = random.randint(1, 9)
                    self.board[x][y] = valid_values[0]
                    valid_values.remove(valid_values[0])

        return self.board
    
    def show(self) -> str:
        """Method to print and return table in ASCII format.
        
        :rtype: str
        """
        table = ''
        cell_length = len(str(9))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(self.board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                        3) * 3 + '+' + '\n'
            table += (('| ' + '{} ' * 3) * 3 + '|').format(*[format_int.format(
                x) if x != 0 else ' ' * cell_length for x in row]) + '\n'
            if i == 9 - 1 or i % 3 == 3 - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                        3) * 3 + '+' + '\n'
        print(table)
        return table
    

    def get_cell(self, cell: tuple[int, int])-> int:
        return self.board[cell[0]][cell[1]]
    
    def _possible_to_swap(self, cell_1: tuple[int, int], cell_2: tuple[int, int])-> bool:
        """
        An internal method to evaluate the ability to rearrange.

        :param cell_1: First cell.
        :type cell_1: tuple[int, int]
        :param cell_2: Second cell.
        :type cell_2: tuple[int, int]
        :return: If the permutation is valid, it returns True. Otherwise False.
        :rtype: bool 
        """
        cell_1_values = self.blank_fillers[cell_1[0]][cell_1[1]]
        cell_2_values = self.blank_fillers[cell_2[0]][cell_2[1]]

        get_cell_1 = self.get_cell(cell_1)
        get_cell_2 = self.get_cell(cell_2)

        num_1 = [i for i in range(1, 10) if cell_1_values[i - 1]]
        num_2 = [i for i in range(1, 10) if cell_2_values[i - 1]]

        left = cell_2_values[self.get_cell(cell_1) - 1]

        right = cell_1_values[self.get_cell(cell_2) - 1]

        if cell_2_values[self.get_cell(cell_1) - 1] and cell_1_values[self.get_cell(cell_2) - 1]:
            return True
        
        return False

    def find_swap(self)-> list[tuple[int, int], int]:
        """
        A method for finding the best permutation.

        :return: List with new board and new goal.
        :rtype: list[list[list[int]], int]
        """

        def swap_cells(board: list[int], first: tuple[int, int], second: tuple[int, int])-> list[int]:
            new_board = copy.deepcopy(board)
            new_board[first[0]][first[1]] = board[second[0]][second[1]]
            new_board[second[0]][second[1]] = board[first[0]][first[1]]
            return new_board

        best_board = self.board
        best_fitness = self.calc_fitness()
        for anchor in self.blanks:
            for stone in self.blanks:
                new_fitness = best_fitness
                if self._possible_to_swap(anchor, stone):
                    new_board = swap_cells(self.board, anchor, stone)
                    new_fitness = self.calc_fitness(board_in=new_board)

                if new_fitness < best_fitness:
                    best_fitness = new_fitness
                    best_board = new_board
                
        return [best_board, best_fitness]



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

    reference = Sudoku(3, 3, board=board)
    reference.show_full()
    reference.solve().show_full()

    ic.disable()
    my_sudoku = Puzzle(board)
    my_sudoku.show()
    ic(my_sudoku.blanks)
    ic(my_sudoku.blank_fillers)

    ic.enable()
    my_sudoku.gen_table()
    my_sudoku.show()

    my_sudoku.gen_table()
    goal = 500

    while goal > 0:
        if goal != 500:
            random.seed(None)
            my_sudoku.gen_table()
            goal = my_sudoku.calc_fitness()


        no_solution = False
        count_iter = 0

        while goal > 0 and not no_solution:
            new_board, new_goal = my_sudoku.find_swap()
            if new_goal == goal:
                no_solution = True
            
            goal = new_goal
            my_sudoku.board = new_board
            count_iter += 1

        if no_solution:
            ic("Решение не было найдено. Остановка в локальном минимуме или на плато.")
            ic(f"Целевая функция: {goal}.")
            ic("Судоку:")
            if ic.enabled:
                my_sudoku.show()
        else:
            print(f"Решение было найдено за {count_iter}")
