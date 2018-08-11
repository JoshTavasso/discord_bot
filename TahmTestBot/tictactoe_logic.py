# STILL INCOMPLETE

# CONSTANTS #

E = '.'
X = 'X'
O = 'O'


class TicTacToeBoard:
    '''
    The TicTacToeBoard implementation contains any and all
    sources of game logic used in a game of TicTacToe
    '''
    def __init__(self):
        self._board = [
            [E, E, E],
            [E, E, E],
            [E, E, E]
            ]

        self._first = X

    def board_state(self):
        '''
        The current state of the board in visual form
        '''
        board_str = f'''
   TIC  TAC  TOE

     1   2   3
   -------------
 1 | {self._board[0][0]} | {self._board[0][1]} | {self._board[0][2]} |
   -------------
 2 | {self._board[1][0]} | {self._board[1][1]} | {self._board[1][2]} |
   -------------
 3 | {self._board[2][0]} | {self._board[2][1]} | {self._board[2][2]} |
   -------------
'''
        return "```" + board_str + "```"

    def clear(self):
        '''
        Clears the board and replaces all cells with '.'
        (or whatever constant 'E' is defined with)
        '''
        for row in range(3):
            for col in range(3):
                self._board[row][col] = E

    def place(self, r, c):
        '''
        Places a piece on the board in the 'r'th row and
        the 'c'th column
        '''
        # make error here
        self._board[r][c] = self._first

    def switch(self):
        '''
        Switches the current player from X to O, or O to X
        '''
        if self._first == X:
            self._first = O
        else:
            self._first = X


def is_not_in_range(r, c):
    # INCOMPLETE
    '''
    Checks if r and c are in range of the rows and columns,
    respectively and returns True or False
    '''
    return False
