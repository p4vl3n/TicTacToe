from os import system
from random import randint
import copy
from sys import maxsize


class TicTacToe:
    EMPTY_FIELD = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'
    FILLED = -maxsize
    AI_LEVEL = 10000  # Added an AI Level variable. With higher number, more scenarios are simulated.

    def __init__(self, size, player):
        self.size = size
        self.board = [[TicTacToe.EMPTY_FIELD for _ in range(size)] for __ in range(size)]
        self.player = player
        self.ai = TicTacToe.PLAYER_X if self.player == TicTacToe.PLAYER_O else TicTacToe.PLAYER_O
        self.empty_field = TicTacToe.EMPTY_FIELD
        self.ai_level = TicTacToe.AI_LEVEL

    def display_board(self):
        system('cls')
        header = [str(i) if i > 0 else self.empty_field for i in range(self.size + 1)]
        print(" | ".join(header))
        for i, r in enumerate(self.board):
            print(f'{i + 1} |', " | ".join(r))
            print('.....' * self.size)

    def swap_player(self, plyr):
        if plyr == self.player:
            return self.ai
        return self.player

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
            if r >= self.size or c >= self.size:  # Checking if selected row by
                print(f'Selected row or column out of range. Please select a row and column from 1 to {self.size}.')
                continue
            if not self.board[r][c] == self.empty_field:
                print('Please select unoccupied field!')
                continue
            return r, c

    # Running through every possible sequence (row, column and diagonal) and calling a checking method on it.
    # If there is a winner, method returns the winner, else it returns EMPTY_FIELD
    def check_for_winner(self, board):
        winner = None
        for sequence in self.get_sequences(board):
            winner = self.winning_sequence(sequence)
            if not winner == TicTacToe.EMPTY_FIELD:
                return winner
        return winner

    # A checking method to find if the sequence consists of the same elements.
    @staticmethod
    def winning_sequence(seq):
        return seq[0] if len(set(seq)) == 1 else TicTacToe.EMPTY_FIELD

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

    def next_best_ai_move_mini_max(self):
        score = 0
        scores_board = [[0 if self.board[r][c] == self.empty_field else self.FILLED for c in range(self.size)]
                        for r in range(self.size)]
        possible_moves = self.get_possible_moves(self.board)
        simulation_board = copy.deepcopy(self.board)
        for move in possible_moves:
            row, col = move
            simulation_board[row][col] = self.ai
            scores_board[row][col] += self.mini_max(simulation_board, self.ai)
            simulation_board[row][col] = self.empty_field

        best_move = self.find_best_move(scores_board)
        return best_move

    # A method to find the best possible next move.
    def next_best_ai_move(self):
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
        for score_prediction in range(self.ai_level):
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

    def find_best_move(self, board):
        best_move = ()
        best_score = -maxsize
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] > best_score:
                    best_move = row, col
                    best_score = board[row][col]

        return best_move

    # The play method initiates the game.
    def play(self):
        self.display_board()

        next_player = TicTacToe.PLAYER_X
        winner = False

        while not self.board_is_full():
            if next_player == self.player:
                row, column = self.valid_user_move()
            else:
                row, column = self.next_best_ai_move_mini_max()
            self.make_a_move(next_player, row, column)
            self.display_board()
            if not self.check_for_winner(self.board) == TicTacToe.EMPTY_FIELD:
                print(f'Congratulations! Player {next_player} wins!')
                winner = True
                break
            next_player = self.swap_player(next_player)

        if not winner:
            print("It's a draw!")


def main():
    while True:
        board_size_choice = input("Choose a board size (3 for 3x3, 4 for 4x4, 5 for 5x5, etc.): ")
        try:  # Checking if players have entered the correct format for the board size.
            board_size = int(board_size_choice)
        except ValueError:  # Prompting players to enter the correct format if they haven't done so.
            print('Please enter a whole number to select the board size.')
            continue
        # level = int(input('Choose a difficulty level (i.e. 10, 50, 100, 200): '))
        user_choice = input('Type X to play first or O to play second: ')
        while user_choice.lower() != 'x' and user_choice.lower() != 'o':
            user_choice = input('Type X to play first or O to play second: ')

        board = TicTacToe(board_size, user_choice.upper())
        board.play()
        play_again = input('Do you want to play again? (Y/N): ')
        if not play_again.upper() == 'Y':
            print('Thanks for playing.')
            break
    exit()


if __name__ == '__main__':
    main()
