'''
Logic.py

Logic implementation used for TTT game using Board.py
'''

from TahmTestBot.Board import Board
from TahmTestBot.Board import E_PIECE, O_PIECE, X_PIECE


class Logic:
    def __init__(self):
        self.game_board = Board(3, 3)

    def game_over(self):
        return False
