from os import system
from random import randint
import copy
from sys import maxsize


class TicTacToe:
    EMPTY_FIELD = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'
    AI_LEVEL = 100  # Added an AI Level variable. With higher number, more scenarios are simulated.

    def __init__(self, size, player):
        self.size = size
        self.board = [[TicTacToe.EMPTY_FIELD for c in range(size)] for r in range(size)]
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
    def check_for_winner(self, board):
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
        score_index = 1
        scores = {}
        for score_prediction in range(self.ai_level):
            player = self.ai
            first_move = None
            is_first_move = True
            simulation_board = copy.deepcopy(self.board)
            possible_moves = self.get_possible_moves(simulation_board)
            score = 0
            while possible_moves:
                r, c = possible_moves[randint(0, len(possible_moves) - 1)]
                if is_first_move:
                    first_move = r, c
                    is_first_move = False
                simulation_board[r][c] = player
                if not self.check_for_winner(simulation_board) == self.empty_field:
                    score = sum([sum([score_index for col in row if col == self.empty_field]) for row in simulation_board])
                    if self.check_for_winner(simulation_board) == self.player:
                        score *= -1
                    break

                player = self.swap_player(player)
                possible_moves = self.get_possible_moves(simulation_board)

            if first_move not in scores:
                scores[first_move] = 0
            scores[first_move] += score

        best_move = ()
        best_score = -maxsize
        for move, score in scores.items():
            if score > best_score:
                best_score = score
                best_move = move

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
                row, column = self.next_best_ai_move()
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

        board = TicTacToe(board_size, user_choice.upper())
        board.play()
        play_again = input('Do you want to play again? (Y/N): ')
        if not play_again.upper() == 'Y':
            print('Thanks for playing.')
            break
    exit()


if __name__ == '__main__':
    main()
