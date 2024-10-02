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
        # x, y = 0, 0
        if direction:
            y = direction["y"]
            x = direction["x"]

            try:
                if game_map[y][x] != 0:
                    if y != -1 and x != -1:

                        game_map[y][x] = 1
                        self.y = y
                        self.x = x
                        game_map[self.y][self.x] = 2

                        if self.y == final[0] and self.x == final[1]:
                            return game_map, True
                        else:
                            return game_map, False

                else:
                    response.status_code = status.HTTP_204_NO_CONTENT
                    return response
            except IndexError:
                pass
            except Exception:
                pass
        else:
            try:
                x = y = 0
                if game_map[self.y + y][self.x + x] != 0:
                    if self.y + y != -1 and self.x + x != -1:

                        game_map[self.y][self.x] = 1
                        self.y += y
                        self.x += x
                        game_map[self.y][self.x] = 2

                        if self.y == final[0] and self.x == final[1]:
                            return game_map, True
                        else:
                            return game_map, False
                else:
                    response.status_code = status.HTTP_204_NO_CONTENT
                    return response
            except IndexError:
                pass
            except Exception:
                pass

        # match direction:
        #     case "right":
        #         x = 1
        #     case "left":
        #         x = -1
        #     case "up":
        #         y = -1
        #     case "down":
        #         y = 1
        #     case _:
        #         pass

        # try:
        #     if game_map[self.y + y][self.x + x] != 0:
        #         if self.y + y != -1 and self.x + x != -1:
        #
        #             game_map[self.y][self.x] = 1
        #             self.y += y
        #             self.x += x
        #             game_map[self.y][self.x] = 2
        #
        #             if self.y == final[0] and self.x == final[1]:
        #                 return game_map, True
        #             else:
        #                 return game_map, False


