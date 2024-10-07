from game_map import Map
from logger import Logger
from player import Player


class Game:
    def __init__(self, rows, columns, logger=Logger()):
        self.map = Map(rows, columns, logger)
        self.map.generate_map()
        self.player = Player(self.map.start_row, self.map.start_col, logger)

    def reset(self):
        self.map.generate_map()
        self.player.items = 0
        self.player.row = self.map.start_row
        self.player.col = self.map.start_col
