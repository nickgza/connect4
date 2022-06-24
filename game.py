import numpy as np
import itertools as it

class MoveError(Exception):
    pass

class Game:
    PLAYER1 = 0
    PLAYER2 = 1

    def __init__(self):
        self.board1 = np.int64(0)
        self.board2 = np.int64(0)
        self.player = self.PLAYER1
        self.past_moves = []
    
    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(row), np.array(['🟡' if one == '1' else '🔴' if two == '1' else '⚪' for one, two in zip(np.binary_repr(self.board1).rjust(42, '0'), np.binary_repr(self.board2).rjust(42, '0'))], dtype=object).reshape((6, 7))))
    
    def make_move(self, column: int, player: int) -> None:
        str_board = np.binary_repr(self.board1 | self.board2).rjust(42, '0')

        if str_board[column] == '1':
            raise MoveError()
        
        self.past_moves.append((self.board1, self.board2, self.player))

        for i in range(column + 35, column - 1, -7):
            if str_board[i] == '0':
                if player == self.PLAYER1:
                    self.board1 |= 1 << (41 - i)
                elif player == self.PLAYER2:
                    self.board2 |= 1 << (41 - i)
                break
    
    def undo_move(self, moves: int = 1) -> None:
        if moves <= 0:
            return

        try:
            for _ in range(moves - 1):
                self.past_moves.pop()
        except IndexError:
            pass

        if not self.past_moves:
            self.board1, self.board2, self.player = np.int64(0), np.int64(0), self.PLAYER1
        else:
            self.board1, self.board2, self.player = self.past_moves.pop()

    def status(self) -> str:
        str_board1 = np.binary_repr(self.board1).rjust(42, '0')
        str_board2 = np.binary_repr(self.board2).rjust(42, '0')

        def check_horizontal(start: int):
            if str_board1[start] == str_board1[start+1] == str_board1[start+2] == str_board1[start+3] == '1':
                return 'PLAYER1'
            if str_board2[start] == str_board2[start+1] == str_board2[start+2] == str_board2[start+3] == '1':
                return 'PLAYER2'
        
        def check_vertical(start: int):
            if str_board1[start] == str_board1[start+7] == str_board1[start+14] == str_board1[start+21] == '1':
                return 'PLAYER1'
            if str_board2[start] == str_board2[start+7] == str_board2[start+14] == str_board2[start+21] == '1':
                return 'PLAYER2'
        
        def check_diagonal_down(start: int):
            if str_board1[start] == str_board1[start+8] == str_board1[start+16] == str_board1[start+24] == '1':
                return 'PLAYER1'
            if str_board2[start] == str_board2[start+8] == str_board2[start+16] == str_board2[start+24] == '1':
                return 'PLAYER2'
        
        def check_diagonal_up(start: int):
            if str_board1[start] == str_board1[start-6] == str_board1[start-12] == str_board1[start-18] == '1':
                return 'PLAYER1'
            if str_board2[start] == str_board2[start-6] == str_board2[start-12] == str_board2[start-18] == '1':
                return 'PLAYER2'

        for start in it.chain(*(range(i, i+4) for i in range(0, 36, 7))):
            result = check_horizontal(start)
            if result in ['PLAYER1', 'PLAYER2']:
                return result
        
        for start in range(0, 21):
            result = check_vertical(start)
            if result in ['PLAYER1', 'PLAYER2']:
                return result
        
        for start in it.chain(*(range(i, i+4) for i in range(0, 15, 7))):
            result = check_diagonal_down(start)
            if result in ['PLAYER1', 'PLAYER2']:
                return result

        for start in it.chain(*(range(i, i+4) for i in range(21, 39, 7))):
            result = check_diagonal_up(start)
            if result in ['PLAYER1', 'PLAYER2']:
                return result
        
        if (self.board1 | self.board2) == 0x3ffffffffff:
            return 'TIE'
        else:
            return 'CONTINUE'
        