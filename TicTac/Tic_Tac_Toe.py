from sys import maxsize
from TicTac.MiniMax import MiniMax
from TicTac.SimpleAi import SimpleAi


class TicTacToe(MiniMax, SimpleAi):
    PLAYER_X = 'X'
    PLAYER_O = 'O'
    FILLED = -maxsize
    LEVEL_MULTIPLIER = 10000
    MINIMAX_LEVEL_BAR = 99999

    def __init__(self, size, player, level):
        super().__init__()
        self.size = size
        self.board = [[self.empty_field for _ in range(size)] for __ in range(size)]
        self.player = player
        self.ai = TicTacToe.PLAYER_X if self.player == TicTacToe.PLAYER_O else TicTacToe.PLAYER_O
        self.level = level * TicTacToe.LEVEL_MULTIPLIER

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