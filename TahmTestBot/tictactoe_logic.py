# STILL INCOMPLETE

LEN = 3


def cell(board, row, col):
    return board[row][col]


def is_empty(board, row, col):
    return cell(board, row, col) == '.'


def is_game_over(board):
    return False