class BoardScanner:
    EMPTY_FIELD = ' '
    BOARD = []
    SIZE = 0

    def __init__(self):
        self.empty_field = BoardScanner.EMPTY_FIELD
        self.board = BoardScanner.BOARD
        self.size = BoardScanner.SIZE
        self.player = None
        self.ai = None

    def check_for_winner(self, board):
        winner = None
        for sequence in self.get_sequences(board):
            winner = self.winning_sequence(sequence)
            if not winner == self.empty_field:
                return winner
        return winner

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
