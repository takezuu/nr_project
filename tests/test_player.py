from game_map import Map
from player import Player
from logger import Logger
import unittest
from map_config import rows_setting, columns_setting


class TestPlayer(unittest.TestCase):

    def setUp(self):
        logger = Logger()
        self.map = Map(rows_setting, columns_setting, logger)
        self.map.generate_map()
        self.player = Player(self.map.start_row, self.map.start_col, logger)

    def test_set_player_position_begin(self):
        self.player.set_player_position(self.map)
        player_position = self.player.get_player_position()
        self.assertEqual(self.map.start_row, player_position["row"], "row is not equal")
        self.assertEqual(self.map.start_col, player_position["col"], "col is not equal")

    def test_set_player_position_new_place(self):
        self.player.set_player_position(self.map)
        player_position = self.player.get_player_position()
        self.assertEqual(self.map.start_row, player_position["row"], "row is not equal")
        self.assertEqual(self.map.start_col, player_position["col"], "col is not equal")
