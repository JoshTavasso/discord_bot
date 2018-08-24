# Board.py
# Board implementation, also used in Logic.py for TTT game

# CONSTANTS #

E_PIECE = '.'
X_PIECE = 'X'
O_PIECE = 'O'


class Board:
    # The Board implementation contains any and all
    # sources of game logic used in a game of TicTacToe
    def __init__(self, row_n: int, col_n: int):
        self._board = create_board(row_n, col_n)

        self._current = X_PIECE
        self._rows = row_n
        self._cols = col_n

    def board(self):
        return self._board

    def current(self):
        return self._current

    def rows(self):
        return self._rows

    def cols(self):
        return self._cols

    def board_state(self):
        # state of the board in string form
        board_str = f'''
   TIC  TAC  TOE

     1   2   3
   -------------
 1 | {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} |
   -------------
 2 | {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} |
   -------------
 3 | {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} |
   -------------
'''
        return "```" + board_str + "```"

    def clear(self):
        # Clears the board and replaces all cells with '.'
        # (or whatever constant 'E_PIECE' is defined with)
        for row in range(self.rows()):
            for col in range(self.cols()):
                self._board[row][col] = E_PIECE

    def is_match(self, r, c):
        return self.view(r, c) == self.current()

    def view(self, r, c):
        # Check and return what's inside the 'r'th row and
        # the 'c'th column of the board
        if not self.in_range(r, c):
            # replace with custom error
            raise IndexError
        return self._board[r][c]

    def place(self, r: int, c: int):
        # Places an X or O on the board in the 'r'th row and
        # the 'c'th column
        if not self.is_valid(r, c):
            # replace with custom error
            raise IndexError
        self._board[r][c] = self.current

    def switch(self):
        # Switches the current player from X to O, or O to X
        if self.current == X_PIECE:
            self._current = O_PIECE
        else:
            self._current = X_PIECE

    def is_valid(self, r, c):
        # Checks if the cell is valid; must be in range and empty
        return self.view(r, c) == E_PIECE

    def in_range(self, r, c):
        # Checks if row and column numbers are within range
        return r in range(self.rows()) and c in range(self.cols())


def create_board(rows, columns):
    # Using a given number of rows and columns, makes a TTT board
    b = []
    for r in range(rows):
        row = []
        for c in range(columns):
            row.append(E_PIECE)
        b.append(row)
    return b
