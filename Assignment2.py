# Prologue Comments
# Title: EECS 348 Assignment 2
# Description: Sudoku puzzle solver, using depth-first-search with backtracking

# Inputs: puzzle1.txt, puzzle2.txt, puzzle3.txt, puzzle4.txt, puzzle5.txt
# Outputs: solution1.txt, solution2.txt, solution3.txt, solution4.txt, solution5.txt

# Collaborators: None
# Sources: Richard Gilchrist, ChatGPT

# Author: Marie Biernacki
# Creation Date: September 5th, 2025

# math module needed for functionality
import math

# function to read the txt file into a string
# SOURCE: Myself
def readFile(string):

    # open the file and read the contents into a string
    with open(string, "r") as txtFile:
        fileString = txtFile.read()

    # convert any underscores to 0s for easy comparison in the future
    zeroString = fileString.replace('_', '0')

    # remove any and all whitespace
    noWhitespace = zeroString.replace(" ","").replace("\t","").replace("\n","")

    # return the modified string
    return noWhitespace


# function to turn the string into a 2D list
# SOURCE: Medium.com "Sudoku Solver with Computer Vision and..." by Richard Gilchrist
def getPuzzle(originalString):
    # the number of rows is equivalent to the square root of the length of the string (square root of 81 = 9)
    num_rows = int(math.sqrt(len(originalString)))

    # sudoku puzzles are square, therefore the number of columns is equal to the number of rows
    num_cols = num_rows

    # create an empty 2D list
    # for every row, create a list within the puzzleBoard list (resulting in a 2D list)
    puzzleBoard = [[] for i in range(num_rows)]

    # use a for loop to extract numbers from the specific row and add to the correct location
    for row in range(num_rows):
        # slice the original string into sections that are the length of num_cols
        ## row * num_cols --> the starting index (inclusive)
        ## (row*num_cols) + num_cols --> the ending index (exclusive)
        row_string = originalString[(row*num_cols):(row*num_cols) + num_cols]

        # for each character in the row_string, convert it into an integer and store it in the corresponding row
        puzzleBoard[row] = [int(num) for num in row_string]

    # return the puzzleBoard
    return puzzleBoard

# class to solve the sudoku puzzles
# SOURCE: Medium.com "Sudoku Solver with Computer Vision and..." by Richard Gilchrist
class SudokuSolver():

    # class constructor
    def __init__(self, puzzle):
        # create the puzzle instance
        self.puzzle = puzzle

        # list to store all puzzle solutions
        self.solutions = []

    # function to find the empty cells in the puzzle, which are represented by 0s
    # pass in the empty_val parameter (which is set to 0)
    # SOURCE: Medium.com "Sudoku Solver with Computer Vision and..." by Richard Gilchrist
    def find_next_empty(self, empty_val: int = 0):

        # set the number of rows equal to the length of the puzzle (the length of the 2D list)
        num_rows = len(self.puzzle)

        # set the number of columns equal to the length of the first row (or list) within the puzzle (2D list)
        num_cols = len(self.puzzle[0])

        # use a nested for loop to iterate through each row and each column in that row
        for row in range(num_rows):
            for col in range(num_cols):
                # if the value at a specific row and column is equal to the empty_val (which is 0)
                # then return the value of that row and column as a tuple (which will be used to find the position)
                if self.puzzle[row][col] == empty_val:
                    return row, col

        # if no empty cells are found, return None
        return None

    # function to check if it is valid to insert a number at a specific position
    # pass in parameters of the puzzle, number, and position
    # SOURCE: Medium.com "Sudoku Solver with Computer Vision and..." by Richard Gilchrist
    def is_valid_number(self, puzzle, number, position):

        # get the size of the puzzle based on the size of the 2D list
        num_rows = len(puzzle)

        # determine the size of the smaller squares within the puzzle by taking the square root of the number of rows
        square_size = int(math.sqrt(num_rows))

        # unpack row and column indices from position tuple
        row_index, col_index = position

        # check if the number is already present in the current row
        if number in puzzle[row_index]:
            # if yes, the number cannot be inserted and is thus invalid
            return False

        # create a list of all current values in the column
        current_column_values = [puzzle[row][col_index] for row in range(num_rows)]

        # check if the number is already present in the current column
        if number in current_column_values:
            # if yes, the number cannot be inserted and is thus invalid
            return False

        # find the smaller square where the position tuple (row_index, col_index) is located
        ## EXAMPLE: if (row_index, col_index) = (5,7) and square_size = 3
        ## square_x_index = 7 // 3 = 2 --> indicates the position is in the third column of the smaller squares
        ## square_y_index = 5 // 3 = 1 --> indicates the position is in the second row of the smaller squares
        ## meaning: the position is in the rightmost column, center row
        square_x_index = col_index // square_size
        square_y_index = row_index // square_size

        # find the starting and ending indices for the rows and columns of the smaller squares
        start_row = square_y_index * square_size
        end_row = start_row + square_size

        start_col = square_x_index * square_size
        end_col = start_col + square_size

        # use a nested for loop to iterate through all positions within the 3 x 3 square
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):

                # check if number is already present in the 3 x 3 square (excluding the current position)
                if puzzle[row][col] == number and (row, col) != position:
                    # if yes, the number cannot be inserted and is thus invalid
                    return False

        # after completing all checks, the number must be valid
        return True


    # recursive function to find all solutions of the puzzle
    # SOURCE: Medium.com "Sudoku Solver with Computer Vision and..." by Richard Gilchrist, ChatGPT
    def solve_all(self):
        # find the next empty position by calling the find_next_empty() method
        next_empty_pos = self.find_next_empty()

        # if there is not another empty position in the puzzle (aka find_next_empty() returns None)
        if not next_empty_pos:
            # create a deep copy of the solved puzzle and store in solutions list
            self.solutions.append([row[:] for row in self.puzzle])

            # do not return true or false, instead continue searching (checking for multiple solutions)
            return

        # store the next empty position to solve
        row, col = next_empty_pos

        # using a for loop, try every valid number (1-9) at the current empty position
        for i in range(1, 10):
            # check if number is valid at the current position
            if self.is_valid_number(self.puzzle, i, (row, col)):
                # if it is valid, tentatively place the number on the board
                self.puzzle[row][col] = i

                # after placing the number, call solve_all() again to continue to fill in empty cells (recursion)
                self.solve_all()

                # reset the position value to 0 in order to try other numbers (backtracking)
                self.puzzle[row][col] = 0


    # function to print the puzzle, regardless of if it is solved or unsolved
    # SOURCE: Myself, ChatGPT
    def print_board(self):

        # set the number of rows equal to the length of the puzzle (the length of the 2D list)
        num_rows = len(self.puzzle)

        # set the number of columns equal to the length of the first row (or list) within the puzzle (2D list)
        num_cols = len(self.puzzle[0])

        # use a nested for loop to iterate through each row and each column in that row
        for row in range(num_rows):
            for col in range(num_cols):
                # obtain the number located at the specific row and column
                number = self.puzzle[row][col]

                # if the col index is less than num_cols - 1 we are NOT at the end of a line
                # use end="" to ensure numbers print on the same line
                if col < num_cols - 1:
                    # if the number is 0, print underscore
                    if number == 0:
                        print(f"_ ", end="")

                    # otherwise print the number
                    else:
                        print(f"{number} ", end="")

                # else the loop reaches the last column, finish with a newline
                else:
                    # if the number is 0 print an underscore
                    if number == 0:
                        print(f"_")

                    # otherwise print the number
                    else:
                        print(f"{number}")


# function to solve puzzle1.txt, puzzle2.txt, puzzle3.txt, puzzle4,txt, puzzle5.txt
# output in the console
# SOURCE: Myself, ChatGPT
def puzzleSolverMain():
    # create a list of the puzzle file names (hardcoded into program)
    fileNames = ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt", "puzzle4.txt", "puzzle5.txt"]

    # iterate through the list
    for i in range(len(fileNames)):
        # read the puzzle file into a clean string
        puzzle_string = readFile(fileNames[i])

        # convert the string into a 2D list
        puzzle_board = getPuzzle(puzzle_string)

        # create a SudokuSolver instance and call the solve_all() method
        solver = SudokuSolver(puzzle_board)
        solver.solve_all()

        # print a divider for clarity
        print("--------------------------------------------------")

        # if we are looking at the first puzzle, no newline is needed
        if i == 0:
            print(f"puzzle{i+1}.txt")
        #otherwise, add a newline
        else:
            print(f"\npuzzle{i+1}.txt")

        # print a heading for clarity
        print(f"\nPuzzle {i+1} Original:")

        # call the print_board() method to print the unsolved board
        solver.print_board()

        # if there is at least one solution
        if solver.solutions:
            # iterate through each solution stored in the list and print
            for idx, solution in enumerate(solver.solutions, 1):
                print(f"\nPuzzle {i+1} Solution #{idx}: ")

                # temporarily replace the solver.puzzle original board with one of the solutions from the list
                solver.puzzle = solution

                # print the solution
                solver.print_board()

        # otherwise, no solution is found
        else:
            print("\nNo solution found")

# function to solve puzzle1.txt, puzzle2.txt, puzzle3.txt, puzzle4,txt, puzzle5.txt
# output in separate txt files
# SOURCE: Myself, ChatGPT
def puzzleSolverToOutFile():
    # create a list of the puzzle file names
    fileNames = ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt", "puzzle4.txt", "puzzle5.txt"]

    # iterate through the list
    for i in range(len(fileNames)):
        # read the puzzle file into a clean string
        puzzle_string = readFile(fileNames[i])

        # convert the string into a 2D list
        puzzle_board = getPuzzle(puzzle_string)

        # create a SudokuSolver instance and call the solve_all() method
        solver = SudokuSolver(puzzle_board)
        solver.solve_all()

        # open a corresponding output file in write mode (solution1.txt, solution2.txt, etc.)
        output_filename = f"solution{i+1}.txt"
        with open(output_filename, "w") as f:

            # write header info
            f.write(f"{fileNames[i]}\n\n")
            f.write(f"Puzzle {i+1} Original:\n")

            # use for loop to write the unsolved puzzle board to the file
            for row in solver.puzzle:
                # for each row, build a string (if num == 0, write underscore, otherwise keep the number)
                # join the numbers with spaces and write to the file
                f.write(" ".join("_" if num == 0 else str(num) for num in row) + "\n")

            # if there is at least one solution
            if solver.solutions:
                #iterate through each solution stored in the list and write to the file
                for idx, solution in enumerate(solver.solutions, 1):
                    # write header into the file
                    f.write(f"\nPuzzle {i+1} Solution #{idx}:\n")

                    # iterate through each row of the solved puzzle board
                    for row in solution:
                        # for each row, build a string
                        # join the numbers with spaces and write to the file
                        f.write(" ".join(str(num) for num in row) + "\n")

            # otherwise, no solution was found
            else:
                # write appropriate message to file
                f.write("\nNo solution found\n")

        # print statement in the console for clarity
        print(f"Results for {fileNames[i]} written to {output_filename}")



if __name__ == '__main__':
    puzzleSolverMain()
    #puzzleSolverToOutFile()

