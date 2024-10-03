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
        only_game_map = game_map.map
        if direction:
            y = direction["row"]
            x = direction["col"]
            print("new coord", y, x)
            available_moves = game_map.find_available_moves()
            try:
                if (y, x) in available_moves:
                    if only_game_map[y][x] != 0:
                        if y >= 0 and x >= 0:
                            only_game_map[self.y][self.x] = 1
                            self.y = y
                            self.x = x
                            only_game_map[y][x] = 2

                            if self.y == final[0] and self.x == final[1]:
                                return True, True
                            else:
                                return True, False

                    return False, False
            except IndexError:
                return False, False
        else:
            only_game_map[self.y][self.x] = 2
