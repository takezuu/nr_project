from typing import Any, Union
from fastapi import status
from map import Map
from fastapi import Response


class Player:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def get_player_position(self) -> dict:
        return {"y": self.y, "x": self.x}

    def set_player_position(self, game_map: Map, direction: dict = None, response: Response = None):
        final = game_map.final
        game_map = game_map.map
        if direction:
            y = direction["y"]
            x = direction["x"]

            try:
                if game_map[y][x] != 0:
                    if y >= 0 and x >= 0:
                        game_map[self.y][self.x] = 1
                        self.y = y
                        self.x = x
                        game_map[y][x] = 2

                        if self.y == final[0] and self.x == final[1]:
                            return game_map, True

                return game_map, False
            except IndexError:
                return game_map, False
        else:
            game_map[self.y][self.x] = 2
            return game_map, False
