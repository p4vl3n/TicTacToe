from TicTac.Tic_Tac_Toe import TicTacToe


def main():
    while True:
        board_size_choice = input("Choose a board size (3 for 3x3, 4 for 4x4, 5 for 5x5, etc.): ")
        try:  # Checking if players have entered the correct format for the board size.
            board_size = int(board_size_choice)
        except ValueError:  # Prompting players to enter the correct format if they haven't done so.
            print('Please enter a whole number to select the board size.')
            continue
        difficulty_level = int(input('Choose difficutly level (1-10): '))
        # level = int(input('Choose a difficulty level (i.e. 10, 50, 100, 200): '))
        user_choice = input('Type X to play first or O to play second: ')
        while user_choice.lower() != 'x' and user_choice.lower() != 'o':
            user_choice = input('Type X to play first or O to play second: ')

        board = TicTacToe(board_size, user_choice.upper(), difficulty_level)
        board.play()
        play_again = input('Do you want to play again? (Y/N): ')
        if not play_again.upper() == 'Y':
            print('Thanks for playing.')
            break
    exit()


if __name__ == '__main__':
    main()
