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
            if self.selected_piece.y == self.move_to.y or self.selected_piece.x == self.move_to.x:
                distance, valid_jump = self.get_lineal_distance()
            else:
                distance, valid_jump = self.get_diagonal_distance()

            if distance == 1:
                self.valid_movement = True
            elif distance == 2:
                self.valid_movement = True if valid_jump else False
            else:
                self.valid_movement = False

            self.valid_input = False
            if self.valid_movement:
                self.move_piece()
                if distance == 1 or (distance == 2 and not self.check_if_can_jump_again()):
                    self.next_player()

    def move_piece(self):
        self.board[self.selected_piece.y][self.selected_piece.x] = 0
        self.board[self.move_to.y][self.move_to.x] = 1 if self.actual_turn == self.player1 else -1

    def is_there_winner(self):
        # TODO: Un jugador gana si se llena el espacio del opuesto y tiene minimo una pieza propia
        return False

    def check_if_can_jump_again(self):
        coords = self.get_cardinals_coords()
        n1, ne1, e1, se1, s1, so1, o1, no1 = coords["n1"], coords["ne1"], coords["e1"], coords["se1"], coords["s1"], coords["so1"], coords["o1"], coords["no1"]
        n2, ne2, e2, se2, s2, so2, o2, no2 = coords["n2"], coords["ne2"], coords["e2"], coords["se2"], coords["s2"], coords["so2"], coords["o2"], coords["no2"]

        for coord in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            if self.board[coord.y][coord.x] != 0:
                if coord == n1 and self.board[n2.y][n2.x] == 0:
                    return True
                elif coord == ne1 and self.board[ne2.y][ne2.x] == 0:
                    return True
                elif coord == e1 and self.board[e2.y][e2.x] == 0:
                    return True
                elif coord == se1 and self.board[se2.y][se2.x] == 0:
                    return True
                elif coord == s1 and self.board[s2.y][s2.x] == 0:
                    return True
                elif coord == so1 and self.board[so2.y][so2.x] == 0:
                    return True
                elif coord == o1 and self.board[o2.y][o2.x] == 0:
                    return True
                elif coord == no1 and self.board[no2.y][no2.x] == 0:
                    return True
        return False

    def get_lineal_distance(self):
        distance = 0
        valid_jump = False

        coords = self.get_cardinals_coords()
        n1, e1, s1, o1 = coords["n1"], coords["e1"], coords["s1"], coords["o1"]
        n2, e2, s2, o2 = coords["n2"], coords["e2"], coords["s2"], coords["o2"]

        if self.move_to in [n1, e1, s1, o1]:
            distance = 1
            valid_jump = True
        elif self.move_to in [n2, e2, s2, o2]:
            distance = 2
            valid_jump = True

            if self.move_to == n2:
                valid_jump = False if self.board[n1.y][n1.x] == 0 else True
            elif self.move_to == e2:
                valid_jump = False if self.board[e1.y][e1.x] == 0 else True
            elif self.move_to == s2:
                valid_jump = False if self.board[s1.y][s1.x] == 0 else True
            elif self.move_to == o2:
                valid_jump = False if self.board[o1.y][o1.x] == 0 else True
            else:
                valid_jump = False
        else:
            distance = 0
            valid_jump = False

        return distance, valid_jump

    def get_diagonal_distance(self):
        distance = 0
        valid_jump = False

        coords = self.get_cardinals_coords()
        ne1, se1, so1, no1 = coords["ne1"], coords["se1"], coords["so1"], coords["no1"]
        ne2, se2, so2, no2 = coords["ne2"], coords["se2"], coords["so2"], coords["no2"]

        if self.move_to in [ne1, se1, so1, no1]:
            distance = 1
            valid_jump = True
        elif self.move_to in [ne2, se2, so2, no2]:
            distance = 2
            valid_jump = True

            if self.move_to == ne2:
                valid_jump = False if self.board[ne1.y][ne1.x] == 0 else True
            elif self.move_to == se2:
                valid_jump = False if self.board[se1.y][se1.x] == 0 else True
            elif self.move_to == so2:
                valid_jump = False if self.board[so1.y][so1.x] == 0 else True
            elif self.move_to == no2:
                valid_jump = False if self.board[no1.y][no1.x] == 0 else True
            else:
                valid_jump = False
        else:
            distance = 0
            valid_jump = False

        return distance, valid_jump

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

    def get_cardinals_coords(self):
        return {
            "n1": Position(self.selected_piece.x, self.selected_piece.y - 1),
            "ne1": Position(self.selected_piece.x + 1, self.selected_piece.y - 1),
            "e1": Position(self.selected_piece.x + 1, self.selected_piece.y),
            "se1": Position(self.selected_piece.x + 1, self.selected_piece.y + 1),
            "s1": Position(self.selected_piece.x, self.selected_piece.y + 1),
            "so1": Position(self.selected_piece.x - 1, self.selected_piece.y + 1),
            "o1": Position(self.selected_piece.x - 1, self.selected_piece.y),
            "no1": Position(self.selected_piece.x - 1, self.selected_piece.y - 1),
            "n2": Position(self.selected_piece.x, self.selected_piece.y - 2),
            "ne2": Position(self.selected_piece.x + 2, self.selected_piece.y - 2),
            "e2": Position(self.selected_piece.x + 2, self.selected_piece.y),
            "se2": Position(self.selected_piece.x + 2, self.selected_piece.y + 2),
            "s2": Position(self.selected_piece.x, self.selected_piece.y + 2),
            "so2": Position(self.selected_piece.x - 2, self.selected_piece.y + 2),
            "o2": Position(self.selected_piece.x - 2, self.selected_piece.y),
            "no2": Position(self.selected_piece.x - 2, self.selected_piece.y - 2)
        }
