import fileinput
import copy
import ntpath
from os import listdir
from os.path import dirname, join, isfile


PUZZLE = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]


class Sudoku:

    def __init__(self, puzzles=None):
        """
        Initialises a sudoku object.

        Parameter:
        puzzles (dict): A dictionary of puzzles, with the key as the file name.
        """

        if not puzzles:
            self.generate_puzzles()
        else:
            self.puzzles = puzzles

    @classmethod
    def from_file(cls, path):
        file_name = ntpath.basename(path)

        puzzle = {file_name: [list(map(int, line.replace('\n', '').replace(' ', '').split(','))) for line in fileinput.input(path)]}
        return cls(puzzle)
    
    @classmethod
    def from_folder(cls, path):
        """
        Load all sudoku puzzles from specific folder.
        """

        file_names = listdir(path)

        puzzles = {}
        for name in file_names:
            puzzle = [list(map(int, line.replace('\n', '').split(','))) for line in fileinput.input(join(path, name))]
            puzzles[name] = puzzle
        
        return cls(puzzles)
    
    def generate_puzzles(self, number=1):
        """
        Create sudoku puzzles.

        Parameter:
        number (int): The number of puzzles to create, default value of 1.
        """

        pass
    
    def get_file_names(self):
        return self.puzzles.keys()
    
    def get_puzzle(self, file_name):
        return self.puzzles[file_name]
    
    def print_puzzles(self):
        """
        Print all puzzles in the correct Sudoku style.
        """

        for puzzle in self.puzzles.values():
            self.print_sudoku(puzzle)
            print()
    
    def print_sudoku(self, puzzle):
        """
        Print a particular puzzle in the Sudoku style.

        Parameter:
        puzzle (list): The puzzle to be printed.
        """

        dim = 13
        row_index = 0
        puzzle_copy = copy.deepcopy(puzzle)
        for i in range(dim):
            if i % 4 == 0:
                if i == 0 or i == dim - 1:
                    print(' '.join(['-'] * dim))
                else:
                    line = ['-'] * dim
                    line[0] = line[dim - 1] = '|'
                    line[4] = line[8] = '+'
                    print(' '.join(line))
            else:
                line = puzzle_copy[row_index]
                line = [x if x != 0 else ' ' for x in line]
                [line.insert(j, '|') for j in range(0, dim, 4)]
                line = list(map(str, line))
                print(' '.join(line))
                row_index += 1

    def solve_puzzles(self, name=None):
        """
        Allows the user to solve all puzzles or a specific puzzle.

        Parameters:
        name (str): The file name of the puzzle to solve, default is to solve all.

        Return:
        boolean: True if successful, False otherwise.
        """

        if not name:
            # solve all puzzles
            for puzzle in self.puzzles.values():
                try:
                    self.print_sudoku(puzzle)
                    succ = self.solve(puzzle)

                    if succ:
                        self.print_sudoku(puzzle)
                    else:
                        print('There is a mistake in the puzzle.')
                except AssertionError as error:
                    print(error)
        else:
            try:
                puzzle = self.puzzles[name]
                self.print_sudoku(puzzle)
                succ = self.solve(puzzle)

                if succ:
                    self.print_sudoku(puzzle)
                else:
                    print('There is a mistake in the puzzle.')
            except AssertionError as assert_error:
                print(assert_error)
            except KeyError as key_error:
                print(f'File does not exist: {key_error}')

    def solve(self, puzzle):
        # check if puzzle is in a valid state
        if not self.valid_state(puzzle):
            return False

        for row in puzzle:
            col_index = 0
            for col in row:
                if col == 0:
                    for i in range(1, 10):
                        row[col_index] = i
                        succ = self.solve(puzzle)

                        if succ:
                            return True
                        elif not succ and i == 9:
                            row[col_index] = 0
                            return False

                col_index += 1
        
        return True

    def valid_state(self, puzzle):
        """
        Checks the current state of the puzzle.

        Parameter:
        puzzle (list): The puzzle being solved.

        Return:
        boolean: True if in valid state, False otherwise.
        """

        # check the key parts to a Sudoku puzzle
        for i in range(9):
            if self.check_square(puzzle, i) and self.check_row(puzzle, i) and self.check_column(puzzle, i):
                continue
            else:
                return False
        
        return True

    def check_square(self, puzzle, square):
        """
        Checks for any duplicates in the specified square.

        Parameters:
        puzzle (list): The puzzle's squares we are checking.
        square (int): The number of the square to check.

        Return:
        boolean: True if valid, False otherwise.
        """

        assert (0 <= square <= 8), 'The index for the square to check was incorrect. No square was found.'

        if 0 <= square < 3:
            row_index = 0
        elif 3 <= square < 6:
            row_index = 3
        elif square < 9:
            row_index = 6

        if square % 3 == 0:
            col_index = 0
        elif square % 3 == 1:
            col_index = 3
        elif square % 3 == 2:
            col_index = 6

        seen = set()
        for row in range(row_index, row_index + 3):
            for col in range(col_index, col_index + 3):
                if puzzle[row][col] == 0:
                    continue
                elif puzzle[row][col] in seen:
                    return False
                else:
                    seen.add(puzzle[row][col])

        return True

    def check_row(self, puzzle, row):
        """
        Checks for duplicates in the rows of the puzzle.

        Parameters:
        puzzle (list): The puzzle that is being checked.
        row (int): The row of the puzzle to be checked for duplicates.

        Return:
        boolean: True if no duplicates, False otherwise.
        """

        seen = set()  # numbers we have seen on the current row

        for col in puzzle[row]:
            if col == 0:
                continue
            elif col in seen:
                return False
            else:
                seen.add(col)

        return True

    def check_column(self, puzzle, column):
        """
        Check if there are any duplicates in the columns of the puzzle.

        Parameters:
        puzzle (list): The puzzle being solved.
        column (int): The index of the column being checked for duplicates.

        Return:
        boolean: True if there are no duplicates, False otherwise.
        """

        seen = set()  # numbers we have seen on the current column

        for i in range(9):
            if puzzle[i][column] == 0:
                continue
            elif puzzle[i][column] in seen:
                return False
            else:
                seen.add(puzzle[i][column])

        return True

def main():
    sudoku = Sudoku.from_folder(join(dirname(__file__), 'puzzles'))
    sudoku.solve_puzzles()


if __name__ == '__main__':
    main()