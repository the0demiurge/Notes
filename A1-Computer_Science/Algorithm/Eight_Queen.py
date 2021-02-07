from copy import deepcopy

SIZE = 8


def print_board(chessboard, board=True, numeric=True):
    if board:
        print('+' + '-' * 2 * SIZE + '+')
        for line in chessboard:
            print('|', *map(lambda x: '  ' if x == 0 else '<>', line), sep='', end='|\n')
        print('+' + '-' * 2 * SIZE + '+')
    if numeric:
        print('BOARD:', *[line.index(1) + 1 for line in chessboard])


def check_board(chessboard, xy):
    x, y = xy
    x -= 1
    while x >= 0:
        if chessboard[x][y]:
            return False
        x -= 1
    x, y = xy
    x, y = x - 1, y + 1
    while 0 <= x < SIZE and 0 <= y < SIZE:
        if chessboard[x][y]:
            return False
        x, y = x - 1, y + 1
    x, y = xy
    x, y = x - 1, y - 1
    while 0 <= x < SIZE and 0 <= y < SIZE:
        if chessboard[x][y]:
            return False
        x, y = x - 1, y - 1
    return True


def eight_queen():
    chessboard = [[0 for i in range(SIZE)] for j in range(SIZE)]
    result = list()

    def helper(i=0):
        if i == SIZE:
            print_board(chessboard)
            result.append(deepcopy(chessboard))
        for j in range(SIZE):
            if check_board(chessboard, (i, j)):
                chessboard[i][j] = 1
                helper(i + 1)
                chessboard[i][j] = 0

    helper()
    return result


if __name__ == "__main__":
    print('NUMS OF SOLUTIONS:', len(eight_queen()))
