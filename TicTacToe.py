from os import system
from time import sleep


class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.board = [[' ' for c in range(size)] for r in range(size)]

    def display_board(self):  # Displaying current board status.
        system('cls')  # Clearing previous view of the board.

        header = [str(i) if i > 0 else ' ' for i in range(self.size + 1)]
        print(" | ".join(header))
        for i, r in enumerate(self.board):
            print(f'{i + 1} |', " | ".join(r))
            print('.....' * self.size)

    @staticmethod
    def swap_player(player):
        if player == 'X':
            return 'O'
        return 'X'

    def make_a_move(self, plyr, r, c):
        self.board[r][c] = plyr

    def valid_user_move(self, selection):
        try:
            row, column = list(map(int, selection))
        except ValueError:
            print('Invalid format. Please follow the specified format.')
            return False
        if row > self.size or column > self.size:  # Checking if selected row by
            print(f'Selected row or column out of range. Please select a row and column from 1 to {self.size}.')
            return False
        return True

    def field_is_empty(self, r, c):
        if self.board[r][c] == ' ':
            return True
        print('Please select unoccupied field!')
        return False

    def player_wins(self, player):
        if self.winner_rows(player):
            return True
        elif self.winner_columns(player):
            return True
        elif self.winner_diagonals(player):
            return True
        return False

    def winner_rows(self, player):
        for row in range(self.size):
            winner = True
            for col in range(self.size):
                if not self.board[row][col] == player:
                    winner = False
                    break
            if winner:
                return winner

    def winner_columns(self, player):
        for col in range(self.size):
            winner = True
            for row in range(self.size):
                if not self.board[row][col] == player:
                    winner = False
                    break
            if winner:
                return winner

    def winner_diagonals(self, player):
        winner = True
        for i in range(self.size):
            if not self.board[i][i] == player:
                winner = False
                break
        if winner:
            return winner

        winner = True
        for i in range(self.size):
            if not self.board[i][-abs(i + 1)] == player:
                winner = False
                break
        return winner

    def board_is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        print("It's a draw!")
        return True

    def play(self):
        self.display_board()
        player = 'X'

        while not self.board_is_full():
            user_selection = input(f'Player {player} choose a row number and a column number to place your move: ')
            if not self.valid_user_move(user_selection):
                continue
            row, column = list(map(int, user_selection))
            row -= 1
            column -= 1
            if not self.field_is_empty(row, column):
                continue
            self.make_a_move(player, row, column)
            self.display_board()
            if self.player_wins(player):
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