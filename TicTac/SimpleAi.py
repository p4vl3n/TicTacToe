from random import randint
import copy
from sys import maxsize
from Helpers import Helpers


class SimpleAi(Helpers):
    FILLED = -maxsize

    def __init__(self):
        super().__init__()

    def simple_ai(self, level):
        """
        Running a for loop through a pre-set number of times.
        Each loop simulates an entire game from the current state of the board.
        At the time of finding a winner, a score is generated based on the number of empty cells.
        A score index is added for each empty cell. The more empty cells, the higher the score.
        However, if the winner is the user, the score is turned into a negative.
        If the simulation ends in a draw, the score remains at default value ('0').

        The first possible move to AI is recorded and added to a dictionary as key and the resulting score
        is added as its value. If the move is already present in the dictionary, we only add the score
        to the already existing value.
        At the end we iterate over all possible moves, and we return the one with the highest score.
        :return:
        """

        scores_board = [[0 if self.board[r][c] == self.EMPTY_FIELD else self.FILLED for c in range(self.size)]
                        for r in range(self.size)]
        for score_prediction in range(level):
            simulation_board = copy.deepcopy(self.board)
            self.simulate(simulation_board)
            condition = self.check_for_winner(simulation_board)
            if condition != self.empty_field:
                additive = 1 if self.ai == condition else -1
                for row_index in range(self.size):
                    for col_index in range(self.size):
                        if self.board[row_index][col_index] != simulation_board[row_index][col_index]:
                            scores_board[row_index][col_index] += additive

        best_move = self.find_best_move(scores_board)
        return best_move

    def simulate(self, board_copy):
        score_index = 1
        player = self.ai
        is_first_move = True
        possible_moves = self.get_possible_moves(board_copy)
        while possible_moves:
            r, c = possible_moves[randint(0, len(possible_moves) - 1)]
            if is_first_move:
                is_first_move = False
            board_copy[r][c] = player
            if not self.check_for_winner(board_copy) == self.empty_field:
                score = sum([sum([score_index for i in board_row if i == self.empty_field]) for board_row in board_copy])
                if self.check_for_winner(board_copy) == self.player:
                    score *= -1
                break

            player = self.swap_player(player)
            possible_moves = self.get_possible_moves(board_copy)

        return board_copy
