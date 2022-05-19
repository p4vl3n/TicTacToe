from sys import maxsize
from TicTac.MiniMax import MiniMax
from TicTac.SimpleAi import SimpleAi


class TicTacToe(MiniMax, SimpleAi):
    LEVEL_MULTIPLIER = 150000
    MINIMAX_LEVEL_BAR = 299999

    def __init__(self, size, player, level):
        super().__init__()
        self.size = size
        self.board = [[self.empty_field for _ in range(size)] for __ in range(size)]
        self.player = player
        self.ai = TicTacToe.PLAYER_X if self.player == TicTacToe.PLAYER_O else TicTacToe.PLAYER_O
        self.level = level * TicTacToe.LEVEL_MULTIPLIER

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

    def play(self):
        self.display_board()

        next_player = TicTacToe.PLAYER_X
        winner = False

        while not self.board_is_full():
            if next_player == self.player:
                row, column = self.valid_user_move()
            else:
                if self.level > TicTacToe.MINIMAX_LEVEL_BAR:
                    row, column = self.ai_move_mini_max()
                else:
                    row, column = self.simple_ai(self.level)
            self.make_a_move(next_player, row, column)
            self.display_board()
            if not self.check_for_winner(self.board) == self.empty_field:
                print(f'Congratulations! Player {next_player} wins!')
                winner = True
                break
            next_player = self.swap_player(next_player)

        if not winner:
            print("It's a draw!")