from os import system
from sys import maxsize
from TicTac.BoardScanner import BoardScanner


class Helpers(BoardScanner):
    def __init__(self):
        super().__init__()

    def display_board(self):
        system('cls')
        header = [str(i) if i > 0 else self.empty_field for i in range(self.size + 1)]
        print(" | ".join(header))
        for i, r in enumerate(self.board):
            print(f'{i + 1} |', " | ".join(r))
            print('.....' * self.size)

    def make_a_move(self, plyr, r, c):
        self.board[r][c] = plyr

    def swap_player(self, plyr):
        if plyr == self.player:
            return self.ai
        return self.player

    def valid_user_move(self):
        while True:
            user_selection = input('Please select a row and column number (i.e. 11, 21, 32, etc): ')
            try:
                r, c = list(map(int, user_selection))
                r -= 1
                c -= 1
            except ValueError:
                print('Invalid format. Please follow the specified format.')
                continue
            if r >= self.size or c >= self.size:  # Checking if selected row by
                print(f'Selected row or column out of range. Please select a row and column from 1 to {self.size}.')
                continue
            if not self.board[r][c] == self.empty_field:
                print('Please select unoccupied field!')
                continue
            return r, c

    def find_best_move(self, board):
        best_move = ()
        best_score = -maxsize
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] > best_score:
                    best_move = row, col
                    best_score = board[row][col]

        return best_move
