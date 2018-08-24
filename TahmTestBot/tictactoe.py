# tictactoe.py
# Logic implementation used for tictactoe game using Board.py

from Board import Board
from Board import E_PIECE, O_PIECE, X_PIECE


class TicTacToe:
    def __init__(self):
        self.game = Board(3, 3)
        self._finished = False

    # HELPER FUNCTIONS

    def three_in_a_row(self, r1, c1, r2, c2):
        # check if there are three X or O pieces in a row
        return self.board.is_match(r1, c1) and self.board.is_match(r2, c2)

    def finished(self):
        return self._finished

    # METHODS

    def game_over(self, r, c):
        # check if the game is over
        if self.finished():
            return True

        # VERTICAL TOP
        if r == 0:
            if self.three_in_a_row(r+1, c, r+2, c):
                return True

        # VERTICAL MID
        elif r == 1:
            if self.three_in_a_row(r-1, c, r+1, c):
                return True

        # VERTICAL BOTTOM
        elif r == 1:
            if self.three_in_a_row(r-2, c, r-1, c):
                return True

        # HORIZONTAL LEFT
        if c == 0:
            if self.three_in_a_row(r, c+1, r, c+2):
                return True

        # HORIZONTAL MID
        elif c == 1:
            if self.three_in_a_row(r, c-1, r, c+1):
                return True

        # HORIZONTAL RIGHT
        elif c == 2:
            if self.three_in_a_row(r, c-2, r, c-1):
                return True

        # DIAGONAL TOP LEFT - BOTTOM RIGHT

        return False

    def turn(self):
        # plays out a turn

        # starts by showing the board
        print(self.game.board_state())

        # Take two ints
        r = 0
        c = 0

        # place on board
        self.game.place(r - 1, c - 1)
        if self.game_over(r - 1, c - 1):
            # raise GameOver Error
            self.end_game()

        # switch turn
        self.game.switch()

    def end_game(self):
        print(self.game.board_state())
        self._finished = True
        return None
