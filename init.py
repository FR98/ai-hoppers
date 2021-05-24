from hoppers import Hoppers
from player import Player
from playerv2 import Player as PlayerV2
from playerv3 import Player as PlayerV3

# player1 = Player(is_ai=True, value=1, depth=1)
# Usar PlayerV3
# player1 = PlayerV3(is_ai=True, value=1, depth=3, multiple_jumps_enabled=True)
# player2 = PlayerV2(is_ai=True, value=-1, depth=2, multiple_jumps_enabled=True)

player1 = PlayerV3(is_ai=True, value=1, depth=1, multiple_jumps_enabled=True)
player2 = PlayerV2(is_ai=True, value=-1, depth=2, multiple_jumps_enabled=True)

Hoppers(player1, player2)
