from game_map import Map
from logger import Logger
from player import Player


class Game:
    def __init__(self, rows, columns, logger=Logger()):
        self.map = Map(rows, columns, logger)
        self.map.generate_map()
        self.player = Player(self.map.start_y, self.map.start_x, logger)

    def reset(self):
        self.map.generate_map()
        self.player.items = 0
        self.player.y = self.map.start_y
        self.player.x = self.map.start_x
