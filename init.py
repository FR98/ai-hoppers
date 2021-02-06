from hoppers import Hoppers
from player import Player

player1 = Player(is_ai=True, value=1, depth=1)
player2 = Player(is_ai=True, value=-1, depth=2)

Hoppers(player1, player2)
