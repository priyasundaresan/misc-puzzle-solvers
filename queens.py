import pprint
import copy
import time

board = lambda: [[0 for _ in range(8)] for _ in range(8)]

def show(board):
    display = []
    for row in board:
        line = []
        for col in row:
            if col == 1:
                line.append('Q')
            else:
                line.append('.')
        display.append(line)
    for line in display:
        print(' '.join(line))

def markup(board, point):
    row, col = point[0], point[1]
    rowPoints = [[row, i] for i in range(8)]
    colPoints = [[i, col] for i in range(8)]
    diagPoints = [[row - i, col - i] for i in range(min(row, col) + 1)]
    diagPoints += [[row - i, col + i] for i in range(min(row, (7 - col)) + 1)]
    diagPoints += [[row + i, col - i] for i in range(min((7 - row), col) + 1)]
    diagPoints += [[row + i, col +   i] for i in range(min((7 - row), (7 - col)) + 1)]
    taken = rowPoints + colPoints + diagPoints
    for [row, col] in taken:
        if not board[row][col]:
            board[row][col] = -1
    return board

solutions = 0

def solve(board, row):
    global solutions
    if row > 7:
        solutions += 1
        print("Soution: ", solutions)
        show(board)
        return
    for col in range(8):
        if not board[row][col]:
            newBoard = copy.deepcopy(board)
            newBoard[row][col] = 1
            newBoard = markup(newBoard, [row, col])
            solve(newBoard, row + 1)
    return

start = time.time()
solve(board(), 0)
print("\nSolved in", time.time() - start, "s\n")
