from sys import maxsize
import copy
from Helpers import find_best_move
from BoardScanner import BoardScanner


class MiniMax(BoardScanner):
    def __init__(self):
        super().__init__()

    """
    The mini_max method iterates over all possible next moves of given TicTacToe board state, 
    and evaluates the state by returning the highest possible score found based on the Minimax algorithm. 
    """

    def mini_max(self, board, player):
        if not self.get_possible_moves(board) and self.check_for_winner(board) == self.EMPTY_FIELD:
            return 0
        elif self.check_for_winner(board) == self.ai:
            return 1 + len(self.get_possible_moves(board))
        elif self.check_for_winner(board) == self.player:
            return -1 - len(self.get_possible_moves(board))

        best_score = maxsize if player == self.ai else -maxsize
        for move in self.get_possible_moves(board):
            row, col = move
            board[row][col] = self.player if player == self.ai else self.ai
            score = self.mini_max(board, self.swap_player(player))
            best_score = min(score, best_score) if player == self.ai else max(score, best_score)
            board[row][col] = self.EMPTY_FIELD
        return best_score


    '''
    The ai_move_mini_max iterates over each available move in the current state of the Tic Tac Toe board,
    and calls the mini_max method to recursively iterate over each branch of every available move. 
    After the evaluation of each move, a pre-generated scores board is updated with the returned evaluation 
    from the mini_max method. 
    At the end, the score board is scanned for the highest evaluated next possible move,
    and the ai_move_mini_max method returns it. 
    '''
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

        best_move = find_best_move(scores_board)
        return best_move
