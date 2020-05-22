import platform
import random
from random import choice
from os import system

from btree import BTree


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def empty_cells(state):
    """
    :param state: a current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


class Board(BTree):
    def __init__(self):
        """Sets the initial state of self, which includes the
                contents of sourceCollection, if it's present."""
        self._root = None
        self.computer_mark = None
        self.human_mark = None

        BTree.__init__(self, root=None, computer_mark=None, human_mark=None)

    def is_right_step(self, state, player_mark):
        """
        :param state: a current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(state, player_mark):
            score = +1
        elif not self.wins(state, player_mark):
            score = -1
        else:
            score = 0

        return score

    def wins(self, state, player):
        """
        :param state: a current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self, state):
        """
        :param state: a current board
        :return: True if anybody wins
        """
        if self.wins(state, self.computer_mark) or self.wins(state, self.human_mark):
            return True

    def possible_move(self, x, y):
        """
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the cell - board[x][y] is empty
        """
        if [x, y] in empty_cells(self.board):
            return True
        else:
            return False

    def set_cell(self, x, y, player):
        """
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.possible_move(x, y):
            self.board[x][y] = player
            return True
        else:
            return False

    def recursion(self, state, depth, player_mark):
        """
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        :param player_mark: an human or a computer
        :return: a score of this possible board
        """

        if depth == 0 or self.game_over(state):
            score = self.is_right_step(state, player_mark)
            return score

        for cell in empty_cells(state):
            state[cell[0]][cell[1]] = self.computer_mark
            score = self.recursion(state, depth - 1, player_mark)
            state[cell[0]][cell[1]] = 0

        return score

    def display(self, state):
        """
        :param state: current state of the board
        """

        str_line = '---------------'

        print('\n' + str_line)
        for row in state:
            for cell in row:
                if cell != 0:
                    symbol = cell
                else:
                    symbol = " "
                print(f'| {symbol} |', end='')
            print('\n' + str_line)

    def computer_step(self, c_choice, game_step):
        """

        :param c_choice: computer's choice X or O
        """
        self.computer_mark = c_choice
        depth = len(empty_cells(self.board))
        if depth == 0 or self.game_over(self.board):
            return

        clean()
        print(f'Computer turn [{c_choice}]')
        self.display(self.board)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])

        else:
            if len(empty_cells(self.board)) >= 2:
                cell1, cell2 = random.sample(empty_cells(self.board), 2)
                state = self.board
                score_left = self.recursion(state, depth, self.computer_mark)
                score_right = self.recursion(state, depth, self.computer_mark)
                if score_left >= score_right:
                    x, y = cell1[0], cell1[1]

                else:
                    x, y = cell2[0], cell2[1]

            else:
                x, y = empty_cells(self.board)[0][0], empty_cells(self.board)[0][1]

        self.set_cell(x, y, c_choice)
        self.add([x, y], game_step)

    def human_step(self, h_choice):
        """
        :param h_choice: human's choice X or O
        """
        self.human_mark = h_choice
        depth = len(empty_cells(self.board))
        if depth == 0 or self.game_over(self.board):
            return

        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        clean()
        print('Human turn [{}]'.format(h_choice))
        self.display(self.board)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.set_cell(coord[0], coord[1], h_choice)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
