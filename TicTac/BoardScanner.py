from os import system
from sys import maxsize


class BoardScanner:
    PLAYER_X = 'X'
    PLAYER_O = 'O'
    EMPTY_FIELD = ' '
    BOARD = []
    SIZE = 0
    FILLED = -maxsize

    def __init__(self):
        self.empty_field = BoardScanner.EMPTY_FIELD
        self.board = BoardScanner.BOARD
        self.size = BoardScanner.SIZE
        self.player = None
        self.ai = None

    def display_board(self):
        system('cls')
        header = [str(i) if i > 0 else self.empty_field for i in range(self.size + 1)]
        print(" | ".join(header))
        for i, r in enumerate(self.board):
            print(f'{i + 1} |', " | ".join(r))
            print('.....' * self.size)

    # A method checking each row, column and diagonal for a winner.
    # If no winner is found, the method returns an empty string.
    def check_for_winner(self, board):
        winner = None
        for sequence in self.get_sequences(board):
            winner = self.winning_sequence(sequence)
            if not winner == self.empty_field:
                return winner
        return winner

    # A method returning the character of the winning player.
    # If no winning player - an empty string is returned.
    def winning_sequence(self, seq):
        return seq[0] if len(set(seq)) == 1 else self.empty_field

    @staticmethod
    def get_rows(board):
        return [row for row in board]

    def get_columns(self, board):
        columns = []
        for c in range(self.size):
            columns.append([board[r][c] for r in range(self.size)])
        return columns

    def get_diagonals(self, board):
        diagonal_one = [board[i][i] for i in range(self.size)]
        diagonal_two = [board[i][-abs(i + 1)] for i in range(self.size)]
        return diagonal_one, diagonal_two

    # A method that gets all rows, columns and diagonals of the board.
    def get_sequences(self, board):
        sequences = []
        sequences.extend(self.get_rows(board))
        sequences.extend(self.get_columns(board))
        sequences.extend(self.get_diagonals(board))
        return sequences

    # Scanning if there are empty cells/fields or if the board is full.
    def board_is_full(self):
        for row in self.board:
            for cell in row:
                if cell == self.empty_field:
                    return False
        return True

    # A method that scans, through a given board and finds all empty fields.
    # Returns a list with every empty field in the board.
    def get_possible_moves(self, board):
        possible_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == self.empty_field:
                    possible_moves.append((row, col))
        return possible_moves

    # Applying the selected move to the board.
    def make_a_move(self, plyr, r, c):
        self.board[r][c] = plyr

    def swap_player(self, plyr):
        if plyr == self.player:
            return self.ai
        return self.player
