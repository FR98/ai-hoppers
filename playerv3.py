"""
---------------------------------------------------------------------------------------------------
    Author
        Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

import xmltodict
from math import sqrt
from random import choice, shuffle
from collections import namedtuple

Position = namedtuple('Position', 'x y')

class Player(object):

    def __init__(self, value, is_ai=False, depth=1, alfa_beta_pruning=True, multiple_jumps_enabled=True, mem=True):
        self.value = value
        self.is_ai = is_ai
        self.depth = depth
        self.alfa_beta_pruning = alfa_beta_pruning
        self.multiple_jumps_enabled = multiple_jumps_enabled
        self.temp = []
        self.mem = mem

    def play(self, board):
        movement_value, best_move = self.minimax(board, self.depth, self.value)
        best_move_xml = self.to_xml(best_move)
        self.temp.append(best_move)
        # return best_move
        return best_move_xml

    def to_xml(self, best_move):
        xml_data = {
            'move': {
                '@distance': best_move['distance'],
                'from': {
                    '@row': best_move['from'].x,
                    '@col': best_move['from'].y,
                },
                'to': {
                    '@row': best_move['to'].x,
                    '@col': best_move['to'].y,
                },
                'path': {
                    'pos': [{ '@row': position.x, '@col': position.y } for position in best_move['path']]
                }
            }
        }

        xml = xmltodict.unparse(xml_data, pretty = True)
        return xml

    def minimax(self, board, depth, maximising=True, alfa=float("-inf"), beta=float("inf")):
        if self.is_there_winner(board):
            return self.eval(board, self.value), None

        if depth == 0:
            random_move = choice(self.get_possible_moves(board, self.value))
            return self.eval(board, self.value), random_move

        best_value = float("-inf") if maximising else float("inf")
        eval_player = self.value if maximising else -self.value
        moves = self.get_possible_moves(board, eval_player)
        best_move = choice(moves)

        moves.reverse()
        moves.sort(key=lambda x: x.get('distance'), reverse=True)
        for move in moves:
            if self.mem and self.three_in_a_row(move): continue
            # Move piece
            piece_value = board[move["from"].y][move["from"].x]
            board[move["from"].y][move["from"].x] = 0
            board[move["to"].y][move["to"].x] = piece_value

            movement_value, _ = self.minimax(board, depth - 1, not maximising, alfa, beta)

            # Move the piece back
            board[move["from"].y][move["from"].x] = piece_value
            board[move["to"].y][move["to"].x] = 0

            if maximising and movement_value > best_value:
                best_move = move
                best_value = movement_value
                alfa = max(alfa, best_value)

            if not maximising and movement_value < best_value:
                best_move = move
                best_value = movement_value
                beta = min(beta, best_value)

            if self.alfa_beta_pruning and beta <= alfa:
                return best_value, best_move

        return best_value, best_move

    def three_in_a_row(self, move):
        if self.temp.count(move) >= 3:
            for i in range(len(self.temp)):
                try:
                    if self.temp[i] == move and self.temp[i+2] == move and self.temp[i+4] == move:
                        return True
                except: pass
        return False

    def eval(self, board, player_value):
        value = 0
        player1_territory, player2_territory = self.get_territories()

        for y in range(len(board)):
            for x in range(len(board[y])):
                position = board[y][x]
                distances = []

                if position == 1:
                    for go_to in player2_territory:
                        if board[go_to.y][go_to.x] == 0:
                            dist_val = self.get_distance(Position(x, y), go_to)
                            # if go_to.x == 1 or go_to.x == 0 or go_to.x == 9 or go_to.x == 8:
                            #     dist_val *= 1.5
                            # if go_to.x == go_to.y:
                            #     dist_val *= 2
                            distances.append(dist_val)
                    # distances = [self.get_distance(Position(x, y), go_to) for go_to in player2_territory if board[go_to.y][go_to.x] == 0]
                    value -= max(distances) if len(distances) else -10

                elif position == -1:
                    for go_to in player1_territory:
                        if board[go_to.y][go_to.x] == 0:
                            dist_val = self.get_distance(Position(x, y), go_to)
                            # if go_to.x == 1 or go_to.x == 0 or go_to.x == 9 or go_to.x == 8:
                            #     dist_val *= -1.5
                            # if go_to.x == go_to.y:
                            #     dist_val *= -2
                            distances.append(dist_val)
                    # distances = [self.get_distance(Position(x, y), go_to) for go_to in player1_territory if board[go_to.y][go_to.x] == 0]
                    value += max(distances) if len(distances) else -10

        if player_value == -1:
            value *= -1

        return value

    def get_distance(self, a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def check_available_jumps(self, board, position):
        coords = self.get_cardinals_coords(position)
        n1, ne1, e1, se1, s1, so1, o1, no1 = coords["n1"], coords["ne1"], coords["e1"], coords["se1"], coords["s1"], coords["so1"], coords["o1"], coords["no1"]
        n2, ne2, e2, se2, s2, so2, o2, no2 = coords["n2"], coords["ne2"], coords["e2"], coords["se2"], coords["s2"], coords["so2"], coords["o2"], coords["no2"]

        available_jumps = 0
        for coord in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            if not coord: continue
            if board[coord.y][coord.x] == 0: continue
            if coord == n1      and n2  and board[n2.y][n2.x] == 0:    available_jumps += 1
            elif coord == ne1   and ne2 and board[ne2.y][ne2.x] == 0:  available_jumps += 1
            elif coord == e1    and e2  and board[e2.y][e2.x] == 0:    available_jumps += 1
            elif coord == se1   and se2 and board[se2.y][se2.x] == 0:  available_jumps += 1
            elif coord == s1    and s2  and board[s2.y][s2.x] == 0:    available_jumps += 1
            elif coord == so1   and so2 and board[so2.y][so2.x] == 0:  available_jumps += 1
            elif coord == o1    and o2  and board[o2.y][o2.x] == 0:    available_jumps += 1
            elif coord == no1   and no2 and board[no2.y][no2.x] == 0:  available_jumps += 1

        return available_jumps

    def is_there_winner(self, board):
        player1_territory_coords, player2_territory_coords = self.get_territories()
        empty_space_in_1, empty_space_in_2 = False, False
        player1_territory = [board[coord.y][coord.x] for coord in player1_territory_coords]
        player2_territory = [board[coord.y][coord.x] for coord in player2_territory_coords]

        if 0 in player1_territory: empty_space_in_1 = True
        if 0 in player2_territory: empty_space_in_2 = True

        if empty_space_in_1 and empty_space_in_2:
            return False
        elif -1 in player1_territory and not empty_space_in_1:
            return True
        elif 1 in player2_territory and not empty_space_in_2:
            return True

        return False

    def get_possible_moves(self, board, player_value, accumulated_moves=[]):
        player1_territory_coords, player2_territory_coords = self.get_territories()
        moves = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] != player_value: continue
                actual_position = Position(x, y)

                if (x == 8 and y == 9) or (x == 9 and y == 8) or (x == 1 and y == 0) or (x == 0 and y == 1) or \
                    (x == 9 and y == 9) or (x == 0 and y == 0) or (x == 8 and y == 8) or (x == 1 and y == 1):
                    if player_value == 1 and actual_position in player2_territory_coords: continue
                    if player_value == -1 and actual_position in player1_territory_coords: continue

                cardinals_coords = self.get_cardinals_coords(actual_position)

                for cardinal in cardinals_coords:
                    if not cardinals_coords[cardinal]: continue
                    is_possible, distance, path = self.is_possible_movement(board, actual_position, cardinals_coords[cardinal])
                    if not is_possible: continue
                    moves.append({
                        "from": actual_position,
                        "to": cardinals_coords[cardinal],
                        "path": path,
                        "distance": distance
                    })

        if self.multiple_jumps_enabled and player_value == self.value:
            for move in moves:
                if move in accumulated_moves: continue
                accumulated_moves.append(move)
                # Move piece
                board[move["from"].y][move["from"].x] = 0
                board[move["to"].y][move["to"].x] = player_value

                available_jumps = self.check_available_jumps(board, move["to"])
                if move["distance"] == 2 and available_jumps > 1:
                    next_moves = self.get_possible_moves(board, player_value, accumulated_moves)

                    for next_move in next_moves:
                        if next_move in moves: continue
                        if move["from"] == next_move["to"]: continue
                        if next_move["distance"] == 2:
                            moves.append({
                                "from": move["from"],
                                "to": next_move["to"],
                                "path": [move["from"], next_move["path"][0], next_move["to"]],
                                "distance": 3
                            })

                # Move the piece back
                board[move["from"].y][move["from"].x] = player_value
                board[move["to"].y][move["to"].x] = 0

        return moves

    def is_possible_movement(self, board, from_position, to_position):
        coords = self.get_cardinals_coords(from_position)
        n1, ne1, e1, se1, s1, so1, o1, no1 = coords["n1"], coords["ne1"], coords["e1"], coords["se1"], coords["s1"], coords["so1"], coords["o1"], coords["no1"]
        n2, ne2, e2, se2, s2, so2, o2, no2 = coords["n2"], coords["ne2"], coords["e2"], coords["se2"], coords["s2"], coords["so2"], coords["o2"], coords["no2"]

        if board[to_position.y][to_position.x] != 0: return False, None, []

        if to_position in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            return True, 1, [from_position, to_position]
        elif to_position in [n2, ne2, e2, se2, s2, so2, o2, no2]:
            if to_position == n2    and board[n1.y][n1.x] != 0:     return True, 2, [from_position, to_position]
            elif to_position == ne2 and board[ne1.y][ne1.x] != 0:   return True, 2, [from_position, to_position]
            elif to_position == e2  and board[e1.y][e1.x] != 0:     return True, 2, [from_position, to_position]
            elif to_position == se2 and board[se1.y][se1.x] != 0:   return True, 2, [from_position, to_position]
            elif to_position == s2  and board[s1.y][s1.x] != 0:     return True, 2, [from_position, to_position]
            elif to_position == so2 and board[so1.y][so1.x] != 0:   return True, 2, [from_position, to_position]
            elif to_position == o2  and board[o1.y][o1.x] != 0:     return True, 2, [from_position, to_position]
            elif to_position == no2 and board[no1.y][no1.x] != 0:   return True, 2, [from_position, to_position]
            else: return False, None, []
        return False, None, []

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

    def get_territories(self):
        player1_territory = [Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3), Position(0, 4), Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3), Position(2, 0), Position(2, 1), Position(2, 2), Position(3, 0), Position(3, 1), Position(4, 0)]
        player2_territory = [Position(9, 5), Position(9, 6), Position(9, 7), Position(9, 8), Position(9, 9), Position(8, 6), Position(8, 7), Position(8, 8), Position(8, 9), Position(7, 7), Position(7, 8), Position(7, 9), Position(6, 8), Position(6, 9), Position(5, 9)]
        return player1_territory, player2_territory
