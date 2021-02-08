from hoppers import Hoppers
from player import Player
from playerv2 import Player as PlayerV2

player1 = Player(is_ai=True, value=1, depth=1)
player2 = PlayerV2(is_ai=True, value=-1, depth=1)

Hoppers(player1, player2)
