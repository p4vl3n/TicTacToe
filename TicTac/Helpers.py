from sys import maxsize

'''
A function dedicated to scanning given score board, 
and returning the highest score from each possible slot. 
'''


def find_best_move(self, board):
    best_move = ()
    best_score = -maxsize
    for row in range(self.size):
        for col in range(self.size):
            if board[row][col] > best_score:
                best_move = row, col
                best_score = board[row][col]

    return best_move
