from game_map import Map
from variables import WALL, CELL, PLAYER, ITEM, FINAL


class Player:
    items = 0

    def __init__(self, y: int, x: int, logger):
        self.row = y
        self.col = x
        self.old_row = None
        self.old_col = None
        self.log = logger.logger
        self.items = 0

    def get_player_position(self) -> dict:
        return {"row": self.row, "col": self.col}

    def set_player_position(self, game_map: Map, direction=None):
        final = game_map.final
        only_game_map = game_map.map
        if direction:
            new_row = direction.row
            new_col = direction.col
            available_moves = self.find_available_moves()
            try:
                if (new_row, new_col) not in available_moves:
                    return False, False

                if only_game_map[new_row][new_col] == WALL or new_row < 0 and new_col < 0:
                    return False, False

                if only_game_map[new_row][new_col] == ITEM:
                    self.items += 1
                    Player.items += 1

                if new_row == final[0] and new_col == final[1] and self.items < 3:
                    return False, False

                only_game_map[self.row][self.col] = CELL
                self.old_row, self.old_col = self.row, self.col
                self.row, self.col = new_row, new_col
                only_game_map[self.row][self.col] = PLAYER
                # проверка, можно ли идти на финал
                if self.row == final[0] and self.col == final[1] and (
                        self.items >= 3):
                    return True, True
                else:
                    return True, False

            except IndexError:
                return False, False
        else:
            # зашита от нерабочей финальной клетки
            if self.row == final[0] and self.col == final[1]:
                only_game_map[self.old_row][self.old_col] = PLAYER
                only_game_map[self.row][self.col] = FINAL
                self.row = self.old_row
                self.col = self.old_col
            # постановка игрока в начале игры
            else:
                only_game_map[self.row][self.col] = PLAYER

    def find_available_moves(self) -> list[tuple]:
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.row + check[0] != -1 and self.col + check[1] != -1:
                    available_moves.append((self.row + check[0], self.col + check[1]))
            except IndexError:
                pass
        return available_moves

    def check_exit(self, game_map: Map):
        if Player.items == game_map.items or self.items >= 3:
            return True
        else:
            return False
