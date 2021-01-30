"""
---------------------------------------------------------------------------------------------------
	Author
	    Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
    Reglas
        Un jugador puede saltar dos casillas solo si esta saltando una pieza
        Un jugador puede moverse en cualquier direccion a una casilla de distancia
        Un jugador gana si se llena el espacio del opuesto y tiene minimo una pieza propia
        Si un jugador salta puede seguir moviendose siempre y cuando pueda seguir saltando
"""

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

        self.pretty_board = PrettyTable()
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

    def play(self):
        while not self.is_there_winner():
            if self.actual_turn == self.player1:
                print("Player 1")
            else:
                print("Player 2")

            while not self.valid_input:
                actual_player_selected_piece = input("Choose a piece to move [x,y]: ")
                self.get_player_input(actual_player_selected_piece, selecting_piece=True)

            self.check_player_movement()
            self.print_board()


    def check_player_movement(self):
        self.valid_input = False

        if self.valid_movement:
            self.next_player()

    def is_there_winner(self):
        return False

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

    def next_player(self):
        self.actual_turn = self.player1 if self.actual_turn == self.player2 else self.player1

    def player_own_position(self, x, y):
        return True if self.board[y][x] == self.actual_turn else False

    def empty_space(self, x, y):
        return True if self.board[y][x] == self.empty else False
    
    def print_board(self):
        row_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.pretty_board.field_names = row_list
        self.pretty_board.add_rows(self.board)
        print(self.pretty_board)
