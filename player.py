"""
---------------------------------------------------------------------------------------------------
    Author
        Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from math import sqrt
from prettytable import PrettyTable
from collections import namedtuple

Position = namedtuple('Position', 'x y')

class Player(object):

    def __init__(self, value, is_ai=False):
        self.value = value
        self.is_ai = is_ai
        self.depth = 2

    def play(self, board):
        return self.minimax(board, self.depth)

    def minimax(self, board, depth, maximising=True, boards=0):
        actual_player_selected_piece = "0,0"
        actual_player_selected_space = "0,0"
        # return actual_player_selected_piece, actual_player_selected_space

        if depth == 0:
            # TODO
            print("TODO: QUE HAGO?")
            # return self.utility_distance(player_to_max), None, prunes, boards
            return "0,0", "0,0"

        if maximising:
            best_val = float("-inf")
            moves = self.get_possible_moves(board, self.value)
        else:
            best_val = float("inf")
            moves = self.get_possible_moves(board, -self.value)

        for move in moves:
            # Move piece
            piece_value = board[move["from"].y][move["from"].x]
            board[move["from"].y][move["from"].x] = 0
            board[move["to"].y][move["to"].x] = piece_value
            boards += 1

            self.minimax(board, depth - 1, not maximising, boards)
            self.print_board(board)

            # Move the piece back
            board[move["from"].y][move["from"].x] = piece_value
            board[move["to"].y][move["to"].x] = 0

            # if maximising and val > best_val:
            #     best_val = val
            #     best_move = (move["from"].loc, to.loc)
            #     a = max(a, val)

            # if not maximising and val < best_val:
            #     best_val = val
            #     best_move = (move["from"].loc, to.loc)
            #     b = min(b, val)

            # if self.ab_enabled and b <= a:
            #     return best_val, best_move, prunes + 1, boards

        # return best_val, best_move, prunes, boards

    def get_possible_moves(self, board, player_value):
        moves = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] != player_value: continue

                actual_position = Position(x, y)
                cardinals_coords = self.get_cardinals_coords(actual_position)

                for cardinal in cardinals_coords:
                    if cardinals_coords[cardinal] and self.is_possible_movement(board, actual_position, cardinals_coords[cardinal]):
                        moves.append({
                            "from": actual_position,
                            "to": cardinals_coords[cardinal]
                        })
        return moves

    def is_possible_movement(self, board, from_position, to_position):
        coords = self.get_cardinals_coords(from_position)
        n1, ne1, e1, se1, s1, so1, o1, no1 = coords["n1"], coords["ne1"], coords["e1"], coords["se1"], coords["s1"], coords["so1"], coords["o1"], coords["no1"]
        n2, ne2, e2, se2, s2, so2, o2, no2 = coords["n2"], coords["ne2"], coords["e2"], coords["se2"], coords["s2"], coords["so2"], coords["o2"], coords["no2"]

        if board[to_position.y][to_position.x] != 0:
            return False

        if to_position in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            return True
        elif to_position in [n2, ne2, e2, se2, s2, so2, o2, no2]:
            if to_position == n2 and board[n1.y][n1.x] != 0:
                return True
            elif to_position == ne2 and board[ne1.y][ne1.x] != 0:
                return True
            elif to_position == e2 and board[e1.y][e1.x] != 0:
                return True
            elif to_position == se2 and board[se1.y][se1.x] != 0:
                return True
            elif to_position == s2 and board[s1.y][s1.x] != 0:
                return True
            elif to_position == so2 and board[so1.y][so1.x] != 0:
                return True
            elif to_position == o2 and board[o1.y][o1.x] != 0:
                return True
            elif to_position == no2 and board[no1.y][no1.x] != 0:
                return True
            else:
                return False
        return False

    def get_cardinals_coords(self, current_position):
        n1 = Position(current_position.x, current_position.y - 1)
        n1 = None if n1.x < 0 or n1.x > 9 or n1.y < 0 or n1.y > 9 else n1
        ne1 = Position(current_position.x + 1, current_position.y - 1)
        ne1 = None if ne1.x < 0 or ne1.x > 9 or ne1.y < 0 or ne1.y > 9 else ne1
        e1 = Position(current_position.x + 1, current_position.y)
        e1 = None if e1.x < 0 or e1.x > 9 or e1.y < 0 or e1.y > 9 else e1
        se1 = Position(current_position.x + 1, current_position.y + 1)
        se1 = None if se1.x < 0 or se1.x > 9 or se1.y < 0 or se1.y > 9 else se1
        s1 = Position(current_position.x, current_position.y + 1)
        s1 = None if s1.x < 0 or s1.x > 9 or s1.y < 0 or s1.y > 9 else s1
        so1 = Position(current_position.x - 1, current_position.y + 1)
        so1 = None if so1.x < 0 or so1.x > 9 or so1.y < 0 or so1.y > 9 else so1
        o1 = Position(current_position.x - 1, current_position.y)
        o1 = None if o1.x < 0 or o1.x > 9 or o1.y < 0 or o1.y > 9 else o1
        no1 = Position(current_position.x - 1, current_position.y - 1)
        no1 = None if no1.x < 0 or no1.x > 9 or no1.y < 0 or no1.y > 9 else no1
        n2 = Position(current_position.x, current_position.y - 2)
        n2 = None if n2.x < 0 or n2.x > 9 or n2.y < 0 or n2.y > 9 else n2
        ne2 = Position(current_position.x + 2, current_position.y - 2)
        ne2 = None if ne2.x < 0 or ne2.x > 9 or ne2.y < 0 or ne2.y > 9 else ne2
        e2 = Position(current_position.x + 2, current_position.y)
        e2 = None if e2.x < 0 or e2.x > 9 or e2.y < 0 or e2.y > 9 else e2
        se2 = Position(current_position.x + 2, current_position.y + 2)
        se2 = None if se2.x < 0 or se2.x > 9 or se2.y < 0 or se2.y > 9 else se2
        s2 = Position(current_position.x, current_position.y + 2)
        s2 = None if s2.x < 0 or s2.x > 9 or s2.y < 0 or s2.y > 9 else s2
        so2 = Position(current_position.x - 2, current_position.y + 2)
        so2 = None if so2.x < 0 or so2.x > 9 or so2.y < 0 or so2.y > 9 else so2
        o2 = Position(current_position.x - 2, current_position.y)
        o2 = None if o2.x < 0 or o2.x > 9 or o2.y < 0 or o2.y > 9 else o2
        no2 = Position(current_position.x - 2, current_position.y - 2)
        no2 = None if no2.x < 0 or no2.x > 9 or no2.y < 0 or no2.y > 9 else no2

        return {"n1": n1, "ne1": ne1, "e1": e1, "se1": se1, "s1": s1, "so1": so1, "o1": o1, "no1": no1, "n2": n2, "ne2": ne2, "e2": e2, "se2": se2, "s2": s2, "so2": so2, "o2": o2, "no2": no2}

    def print_board(self, board):
        row_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        pretty_board = PrettyTable()
        pretty_board.field_names = row_list
        pretty_board.add_rows(board)
        print(pretty_board)
