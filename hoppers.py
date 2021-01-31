"""
---------------------------------------------------------------------------------------------------
	Author
	    Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from math import sqrt
from collections import namedtuple
from prettytable import PrettyTable

Position = namedtuple('Position', 'x y')

class Hoppers(object):

    def __init__(self, use_bot=False):
        self.board = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
        ]

        self.empty = 0
        self.player1 = 1
        self.player2 = -1
        self.actual_turn = self.player1
        self.valid_input = False
        self.selected_piece = None
        self.move_to = None
        self.valid_movement = True

        self.use_bot = use_bot
        self.play()

    def next_player(self):
        self.actual_turn = 1 if self.actual_turn == self.player2 else -1

    def play(self):
        self.print_board()

        while not self.is_there_winner():
            if self.actual_turn == self.player1:
                print("Player 1")
            else:
                print("Player 2")

            actual_player_selected_piece = input("Choose a piece to move [x,y]: ")
            self.get_player_input(actual_player_selected_piece, selecting_piece=True)

            if self.valid_input:
                actual_player_selected_space = input("Choose a space to move to [x,y]: ")
                self.get_player_input(actual_player_selected_space, selecting_piece=False)
                self.check_player_movement()
            self.print_board()

    def check_player_movement(self):
        distance = 0
        self.valid_movement = False

        if self.valid_input:
            if self.selected_piece.y == self.move_to.y:
                distance = sqrt((self.selected_piece.x - self.move_to.x) ** 2)
            elif self.selected_piece.x == self.move_to.x:
                distance = sqrt((self.selected_piece.y - self.move_to.y) ** 2)
            else:
                distance = self.get_diagonal_distance()

            distance = int(distance)

            if distance == 1:
                self.valid_movement = True
            elif distance == 2:
                # Un jugador puede saltar dos casillas solo si esta saltando una pieza
                # Si un jugador salta puede seguir moviendose siempre y cuando pueda seguir saltando
                self.valid_movement = True
            else:
                self.valid_movement = False

            self.valid_input = False
            if self.valid_movement:
                self.move_piece()
                self.next_player()

    def move_piece(self):
        self.board[self.selected_piece.y][self.selected_piece.x] = 0
        self.board[self.move_to.y][self.move_to.x] = 1 if self.actual_turn == self.player1 else -1

    def is_there_winner(self):
        # TODO: Un jugador gana si se llena el espacio del opuesto y tiene minimo una pieza propia
        return False

    def get_diagonal_distance(self):
        distance = 0

        diagonals1 = [
            Position(self.selected_piece.x + 1, self.selected_piece.y - 1),
            Position(self.selected_piece.x + 1, self.selected_piece.y + 1),
            Position(self.selected_piece.x - 1, self.selected_piece.y + 1),
            Position(self.selected_piece.x - 1, self.selected_piece.y - 1)
        ]

        diagonals2 = [
            Position(self.selected_piece.x + 2, self.selected_piece.y - 2),
            Position(self.selected_piece.x + 2, self.selected_piece.y + 2),
            Position(self.selected_piece.x - 2, self.selected_piece.y + 2),
            Position(self.selected_piece.x - 2, self.selected_piece.y - 2)
        ]

        if self.move_to in diagonals1:
            distance = 1
        elif self.move_to in diagonals2:
            distance = 2
        else:
            distance = 0

        return distance

    def get_player_input(self, player_input, selecting_piece):
        try:
            x, y = player_input.split(",")
            x, y = int(x), int(y)

            if x >= 0 and x <= len(self.board[0]) and y >= 0 and y <= len(self.board[0]):

                if selecting_piece:
                    if self.player_own_position(x, y):
                        self.valid_input = True
                        self.selected_piece = Position(x, y)
                    else:
                        self.valid_input = False
                else:
                    if self.empty_space(x, y):
                        self.valid_input = True
                        self.move_to = Position(x, y)
                    else:
                        self.valid_input = False

            else:
                self.valid_input = False
        except:
            self.valid_input = False

    def player_own_position(self, x, y):
        return True if self.board[y][x] == self.actual_turn else False

    def empty_space(self, x, y):
        return True if self.board[y][x] == self.empty else False
    
    def print_board(self):
        row_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        pretty_board = PrettyTable()
        pretty_board.field_names = row_list
        pretty_board.add_rows(self.board)
        print(pretty_board)
