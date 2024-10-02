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

    def set_player_position(self, game_map: Map, direction: str = None, response: Response = None) -> (Union[
                                                                                                           Any, bool] |
                                                                                                       Response | None):
        x, y = 0, 0
        final = game_map.final
        game_map = game_map.map

        match direction:
            case "right":
                x = 1
            case "left":
                x = -1
            case "up":
                y = -1
            case "down":
                y = 1
            case _:
                pass

        try:
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
