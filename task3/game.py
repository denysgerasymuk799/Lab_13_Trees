from board import clean, Board, empty_cells


def check_user_input():
    h_choice = ""
    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\n(if you want to break - CTRL + D)\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    return h_choice


def start_game():
    """
    Main function that calls all functions
    """
    clean()
    first = ''

    h_choice = check_user_input()
    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    game_board = Board()
    game_board.computer_mark = c_choice

    game_step = 0
    # Main loop of this game
    while len(empty_cells(game_board.board)) > 0 and\
            not game_board.game_over(game_board.board):
        if first == 'N':
            game_board.computer_step(c_choice, game_step)
            first = ''

        game_step += 1

        game_board.human_step(h_choice)
        game_board.computer_step(c_choice, game_step)
        game_step += 1

    # Game over message
    if game_board.wins(game_board.board, h_choice):
        clean()
        print(f'Human turn [{h_choice}]')
        game_board.display(game_board.board)
        print('My congritulations - YOU WIN!')
    elif game_board.wins(game_board.board, c_choice):
        clean()
        print(f'Computer turn [{c_choice}]')
        game_board.display(game_board.board)
        print('Sorry, but YOU LOSE!')
    else:
        clean()
        game_board.display(game_board.board)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    start_game()
