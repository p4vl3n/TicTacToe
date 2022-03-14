from os import system
from time import sleep


class TicTacToe:
    EMPTY_FIELD = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    def __init__(self, size):
        self.size = size
        self.board = [[TicTacToe.EMPTY_FIELD for c in range(size)] for r in range(size)]

    def display_board(self):
        system('cls')
        header = [str(i) if i > 0 else TicTacToe.EMPTY_FIELD for i in range(self.size + 1)]
        print(" | ".join(header))
        for i, r in enumerate(self.board):
            print(f'{i + 1} |', " | ".join(r))
            print('.....' * self.size)

    @staticmethod
    def swap_player(plyr):
        if plyr == TicTacToe.PLAYER_X:
            return TicTacToe.PLAYER_O
        return TicTacToe.PLAYER_X

    # Applying player's move.
    def make_a_move(self, plyr, r, c):
        self.board[r][c] = plyr

    # Checking if player's selection is in valid format.
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
            if r > self.size or c > self.size:  # Checking if selected row by
                print(f'Selected row or column out of range. Please select a row and column from 1 to {self.size}.')
                continue
            if not self.board[r][c] == TicTacToe.EMPTY_FIELD:
                print('Please select unoccupied field!')
                continue
            return r, c

    def check_for_winner(self):
        for sequence in self.get_sequences():
            winner = self.winning_sequence(sequence)
            if not winner == TicTacToe.EMPTY_FIELD:
                return winner
        return winner

    @staticmethod
    def winning_sequence(seq):
        return seq[0] if len(set(seq)) == 1 else TicTacToe.EMPTY_FIELD

    def get_rows(self):
        return [row for row in self.board]

    def get_columns(self):
        columns = []
        for c in range(self.size):
            columns.append(self.board[r][c] for r in range(self.size))
        return columns

    def get_diagonals(self):
        diagonal_one = [self.board[i][i] for i in range(self.size)]
        diagonal_two = [self.board[i][-abs(i + 1)] for i in range(self.size)]
        return diagonal_one, diagonal_two

    def get_sequences(self):
        sequences = []
        sequences.extend(self.get_rows())
        sequences.extend(self.get_columns())
        sequences.extend(self.get_diagonals())
        return sequences

    # Scanning if there are empty cells/fields or if the board is full.
    def board_is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        print("It's a draw!")
        return True

    # The play method initiates the game.
    def play(self):
        self.display_board()
        player = TicTacToe.PLAYER_X

        while not self.board_is_full():
            row, column = self.valid_user_move()
            self.make_a_move(player, row, column)
            self.display_board()
            if not self.check_for_winner() == TicTacToe.EMPTY_FIELD:
                print(f'Congratulations! Player {player} wins!')
                break
            player = self.swap_player(player)


def main():
    while True:
        board_size_choice = input("Choose a board size (3 for 3x3, 4 for 4x4, 5 for 5x5, etc.): ")
        try:  # Checking if players have entered the correct format for the board size.
            board_size = int(board_size_choice)
            board = TicTacToe(board_size)  # If they have, we initialize the game.
        except ValueError:  # Prompting players to enter the correct format if they haven't done so.
            print('Please enter a whole number to select the board size.')
            continue
        board.play()
        play_again = input('Do you want to play again? (Y/N): ')
        if not play_again.upper() == 'Y':
            print('Thanks for playing.')
            break
    exit()


if __name__ == '__main__':
    main()
