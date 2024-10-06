from game_map import Map
from variables import WALL, CELL, PLAYER, ITEM, FINAL


class Player:
    items = 0

    def __init__(self, y: int, x: int, logger):
        self.y = y
        self.x = x
        self.old_y = None
        self.old_x = None
        self.log = logger.logger
        self.items = 0

    def get_player_position(self) -> dict:
        return {"y": self.y, "x": self.x}

    def set_player_position(self, game_map: Map, direction=None):
        final = game_map.final
        only_game_map = game_map.map
        if direction:
            y = direction.row
            x = direction.col
            available_moves = self.find_available_moves()
            try:
                if (y, x) in available_moves:
                    if only_game_map[y][x] != WALL:
                        if y >= 0 and x >= 0:
                            if only_game_map[y][x] == ITEM:
                                self.items += 1
                                Player.items += 1
                            if y == final[0] and x == final[1] and self.items < 3:
                                return False, False

                            only_game_map[self.y][self.x] = CELL
                            self.old_y = self.y
                            self.old_x = self.x
                            self.y = y
                            self.x = x
                            only_game_map[self.y][self.x] = PLAYER
                            # проверка, можно ли идти на финланл
                            if self.y == final[0] and self.x == final[1] and (
                                    self.items >= 3 or Player.items == game_map.items):
                                return True, True
                            elif self.y == final[0] and self.x == final[1] and (
                                    self.items < 3 or Player.items < game_map.items):
                                return False, False
                            else:
                                return True, False

                    return False, False
            except IndexError:
                return False, False
        else:
            # зашита от нерабочей финальной клетки
            if self.y == final[0] and self.x == final[1]:
                only_game_map[self.old_y][self.old_x] = PLAYER
                only_game_map[self.y][self.x] = FINAL
                self.y = self.old_y
                self.x = self.old_x
            # постановка игрока в начале игры
            else:
                only_game_map[self.y][self.x] = PLAYER

    def find_available_moves(self) -> list[tuple]:
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.y + check[0] != -1 and self.x + check[1] != -1:
                    available_moves.append((self.y + check[0], self.x + check[1]))
            except IndexError:
                pass
        return available_moves

    def check_exit(self, game_map: Map):
        print("all", Player.items, "self", self.items)
        if Player.items == game_map.items or self.items >= 3:
            return True
        else:
            return False
