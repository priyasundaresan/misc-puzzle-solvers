import pprint # For printing the grid nicely
import time # To display how long it takes to solve a puzzle
import argparse

file = open('sudokutests.txt', 'r')
lines = [line.strip() for line in file.readlines()]
file.close()
testsCache = {int(line[5:]): [] for line in lines if 'Grid' in line}
grids = [line for line in lines if lines.index(line) % 10]
key = 1
for i in range(0, len(grids), 9):
    grid = [list(map(lambda x: int(x), list(i))) for i in grids[i: i+9]]
    testsCache[key] = grid
    key += 1

def findUnknowns(grid):
    """ Finds all points in a grid that are unknown (represented as 0)
        A point is represented as a 2-element list [row, col] """
    def allIndices(lst, item):
        yield from [i for i, x in enumerate(lst) if x == item]
    for row in grid:
        for col in allIndices(row, 0):
            yield [grid.index(row), col]

def orderUnknowns(points, grid):
    """ Orders a list of unknown points by ascending order of how many candidates they have.
        Points that are constrained to only contain 1 number for example should go first.
        Purely an optimization to the solve function """
    return sorted(points, key=lambda point: len(candidates(point, grid)))

def defineBox(point):
    """ Returns the list of points within a 3 x 3 box that contains a given point """
    row, col = point[0], point[1]
    if row % 3 == 0: rowRange = [row, row+1, row+2]
    elif row % 3 == 1: rowRange = [row-1, row, row+1]
    elif row % 3 == 2: rowRange = [row-2, row-1, row]
    if col % 3 == 0: colRange = [col, col+1, col+2]
    elif col % 3 == 1: colRange = [col-1, col, col+1]
    elif col % 3 == 2: colRange = [col-2, col-1, col]
    boxPoints = []
    for i in rowRange:
        for j in colRange:
            boxPoints.append([i,j])
    return boxPoints

def candidates(point, grid):
    """ Returns all possible numbers that could go in a point, i.e. numbers 1 - 10 that are NOT:
        - in the same row as the point
        - in the same column as the point
        - in the same 3 x 3 box as the point
    """
    row, col = point[0], point[1]
    colNums = [row[col] for row in grid]
    rowNums = grid[row]
    boxNums = [grid[row][col] for [row, col] in defineBox(point)]
    taken = set([i for i in colNums + rowNums + boxNums if i])
    return [i for i in range(1, 10) if not i in taken]

solutionCount = 0 # Keeps track of all possible solutions to a given puzzle

def solve(grid):
    """ Returns ALL possible solutions to a puzzle. """
    global solutionCount
    for point in orderUnknowns(list(findUnknowns(grid)), grid):
        row, col = point[0], point[1]
        for candidate in candidates(point, grid):
            grid[row][col] = candidate
            solve(grid)
        # If there are no candidates for a point, this means we have made an error, so reset the point to blank and start fresh
        grid[row][col] = 0
        return
    # At this point, we have iterated through all the unknown points and reached a solution, print it
    solutionCount += 1
    print("\nSolution", solutionCount)
    pprint.pprint(grid)

""" To run the program at the command line.
    eg 1) $ python3 sudoku.py -t 51 # Solves test case 51
    eg 2) $ python3 sudoku.py -c # Prints out all test cases """
parser = argparse.ArgumentParser(description='Solve a Sudoku Puzzle')
parser.add_argument('-t', '--test', type=int, metavar='', help='enter a test case puzzle | (eg: -t 51) runs test 51')
parser.add_argument('-c', '--cases', action='store_true', help='print all test cases')
args = parser.parse_args()

""" Gets a puzzle from user, parses and orders cipherwords, and solves puzzle."""
if __name__ == '__main__':
    if args.cases:
        pprint.pprint(testsCache) # Prints the suite of test cases
    elif args.test:
        grid = testsCache[args.test]
        start = time.time()
        solve(grid)
        print("\nSolved in:", time.time() - start, "s")
