from map import Map


class Player:

    def __init__(self, y: int, x: int, logger):
        self.y = y
        self.x = x
        self.old_y = None
        self.old_x = None
        self.log = logger.logger

    def get_player_position(self) -> dict:
        return {"y": self.y, "x": self.x}

    def set_player_position(self, game_map: Map, direction=None):
        self.log.info(f"new coords {self.y} {self.x}")
        final = game_map.final
        only_game_map = game_map.map
        if direction:
            y = direction.row
            x = direction.col
            available_moves = self.find_available_moves()
            try:
                if (y, x) in available_moves:
                    if only_game_map[y][x] != 0:
                        if y >= 0 and x >= 0:
                            only_game_map[self.y][self.x] = 1
                            self.old_y = self.y
                            self.old_x = self.x
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
            if self.y == final[0] and self.x == final[1]:
                only_game_map[self.old_y][self.old_x] = 2
                only_game_map[self.y][self.x] = 3
                self.y = self.old_y
                self.x = self.old_x
            else:
                only_game_map[self.y][self.x] = 2

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
