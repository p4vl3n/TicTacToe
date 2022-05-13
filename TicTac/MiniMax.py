from sys import maxsize
import copy
from Helpers import Helpers


class MiniMax(Helpers):
    def __init__(self):
        super().__init__()

    def mini_max(self, board, player):
        if not self.get_possible_moves(board) and self.check_for_winner(board) == self.EMPTY_FIELD:
            return 0
        elif self.check_for_winner(board) == self.ai:
            return 1 + len(self.get_possible_moves(board))
        elif self.check_for_winner(board) == self.player:
            return -1 - len(self.get_possible_moves(board))

        if player == self.player:
            best_score = -maxsize
            for move in self.get_possible_moves(board):
                row, col = move
                board[row][col] = self.ai
                score = self.mini_max(board, self.swap_player(player))
                if score > best_score:
                    best_score = score
                board[row][col] = self.EMPTY_FIELD
        else:
            best_score = maxsize
            for move in self.get_possible_moves(board):
                row, col = move
                board[row][col] = self.player
                score = self.mini_max(board, self.swap_player(player))
                if score < best_score:
                    best_score = score
                board[row][col] = self.EMPTY_FIELD
        return best_score

    def ai_move_mini_max(self):
        scores_board = [[0 if self.board[r][c] == self.EMPTY_FIELD else self.FILLED for c in range(self.size)]
                        for r in range(self.size)]
        possible_moves = self.get_possible_moves(self.board)
        simulation_board = copy.deepcopy(self.board)
        for move in possible_moves:
            row, col = move
            simulation_board[row][col] = self.ai
            scores_board[row][col] += self.mini_max(simulation_board, self.ai)
            simulation_board[row][col] = self.EMPTY_FIELD

        best_move = self.find_best_move(scores_board)
        return best_move
