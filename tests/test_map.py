from game_map import Map
from logger import Logger
import unittest
from map_config import rows_setting, columns_setting


class TestMap(unittest.TestCase):

    def setUp(self):
        logger = Logger()
        self.map = Map(rows_setting, columns_setting, logger)

    def test_generate_empty_map(self):
        self.map.create_empty_map()
        map_len = len(self.map.map)
        self.assertGreater(map_len, 0, "map <= 0 should be > 0")

    def test_generate_start_position(self):
        self.map.create_empty_map()
        self.map.generate_start_position()
        self.assertIsNotNone(self.map.start_col, "start col is None")
        self.assertIsNotNone(self.map.start_row, "start row is None")

    def test_generate_path(self):
        self.map.create_empty_map()
        self.map.generate_start_position()
        self.map.generate_path()

        path = False
        for row in self.map.map:
            if 1 in row:
                path = True
        self.assertTrue(path, "there is no generated path")

    def test_generate_false_path(self):
        self.map.create_empty_map()
        self.map.generate_start_position()
        self.map.generate_path()
        self.map.generate_false_path()

        false_path = False
        for row in self.map.map:
            if 4 in row:
                false_path = True
        self.assertTrue(false_path, "there is no false generated path")

    def test_item_respawn(self):
        self.map.create_empty_map()
        self.map.generate_start_position()
        self.map.generate_path()
        self.map.generate_false_path()
        while len(self.map.final_invalid_moves) < 5:
            self.map.erase_map()
            self.map.generate_path()
            self.map.generate_false_path()
        self.map.item_respawn()

        item = False
        for row in self.map.map:
            if 5 in row:
                item = True
        self.assertTrue(item, "there are no items")

    def test_convert_map(self):
        self.map.create_empty_map()
        self.map.generate_start_position()
        self.map.generate_path()
        self.map.generate_false_path()
        self.map.convert_map()

        cells = True
        for row in self.map.map:
            if 4 in row:
                cells = False
        self.assertTrue(cells, "there are no items")


if __name__ == "__main__":
    unittest.main()
