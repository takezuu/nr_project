import random

from map_config import path_setting, false_path_setting
from variables import WALL, CELL, OUT, FINAL, EXTRA_PATH, ITEM
from logger import Logger


class Map:

    def __init__(self, rows: int, columns: int, logger: Logger):
        self.items = 0
        self.columns = columns
        self.rows = rows
        self.min_row = 0
        self.max_row = None
        self.min_column = 0
        self.max_column = None
        self.row = None
        self.col = None
        self.map = None
        self.final = tuple()
        self.final_invalid_moves = []
        self.start_row = None
        self.start_col = None
        self.completed = False
        self.logger = logger.logger
        self.logger.info("Экземпляр карты создан")
        self.logger.info(f"Размеры карты rows={self.rows}, columns={self.columns}")

    def create_empty_map(self) -> None:
        self.map = [[WALL for _ in range(self.columns)] for _ in range(self.rows)]

    def print_map(self) -> None:
        for n, row in enumerate(self.map):
            print(f"Row {n}: {row}")
        print("\n")

    def generate_start_position(self) -> None:
        self.max_row = len(self.map) - 1
        self.max_column = len(self.map[0]) - 1

        self.start_row = self.row = random.randint(self.min_row, self.max_row)
        self.start_col = self.col = random.randint(self.min_column, self.max_column)

        if self.row != self.min_row or self.row != self.max_row:
            self.start_col = self.col = random.choice([self.min_column, self.max_column])

    def generate_path(self) -> None:
        self.map[self.row][self.col] = CELL
        path_length = 0
        while path_length < path_setting:
            loop_flag = True
            while loop_flag:
                path_length += 1
                moves = self.find_available_moves()
                loop_flag = self.select_move(moves)

                if loop_flag is False and path_length < path_setting:
                    path_length = 0
                    self.create_empty_map()
                    self.generate_start_position()
                    self.map[self.row][self.col] = CELL

    def find_available_moves(self) -> list[tuple]:
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.map[self.row + check[0]][self.col + check[1]] == WALL:
                    if (self.row + check[0]) != OUT and (self.col + check[1]) != OUT:
                        available_moves.append((self.row + check[0], self.col + check[1]))
            except IndexError:
                pass
        return available_moves

    def select_move(self, moves: list[tuple]) -> bool:
        check_tuples = [(0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0),
                        (1, 1)]  # координаты для выбора хода, проверка по оценки суммы единиц и стартового хода
        final_moves = []
        try:
            for move in moves:
                score = 0
                for check in check_tuples:
                    new_y = move[0] + check[0]
                    new_x = move[1] + check[1]
                    if 0 <= new_y < self.max_row + 1 and 0 <= new_x < self.max_column + 1:
                        if self.map[new_y][new_x] == CELL:
                            score += 1

                if score <= 2:

                    if move not in final_moves:
                        final_moves.append(move)
        except IndexError:
            pass
        if final_moves:
            self.row, self.col = random.choice(final_moves)
            self.map[self.row][self.col] = CELL
            return True
        else:
            self.map[self.row][self.col] = FINAL
            self.final = (self.row, self.col)
            return False

    def find_right_positions(self):
        false_positions = []
        for row in self.map:
            zero_indices = [index for index, element in enumerate(row) if element == CELL or element == FINAL]
            for index in zero_indices:
                false_positions.append((self.map.index(row), index))
        return false_positions

    def find_available_false_moves(self, move) -> list[tuple]:
        y = move[0]
        x = move[1]
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.map[y + check[0]][x + check[1]] == WALL:
                    if (y + check[0]) != OUT and (x + check[1]) != OUT:
                        available_moves.append((y + check[0], x + check[1]))
            except IndexError:
                pass
        return available_moves

    def select_false_move(self, moves: list[tuple]):
        check_tuples = [(0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0),
                        (1, 1)]  # координаты для выбора хода, проверка по оценки суммы единиц и стартового хода
        final_moves = []
        try:
            for move in moves:
                score = 0
                for check in check_tuples:
                    new_y = move[0] + check[0]
                    new_x = move[1] + check[1]
                    if 0 <= new_y < self.max_row + 1 and 0 <= new_x < self.max_column + 1:
                        if self.map[new_y][new_x] == CELL or self.map[new_y][new_x] == EXTRA_PATH:
                            score += 1

                if score <= 2:
                    final_moves.append(move)

        except IndexError:
            pass

        if final_moves:
            move = random.choice(final_moves)
            self.map[move[0]][move[1]] = EXTRA_PATH
            return move, True
        else:
            return final_moves, False

    def generate_false_path(self):
        right_positions = self.find_right_positions()
        for position in right_positions:
            moves = self.find_available_false_moves(position)
            move, flag = self.select_false_move(moves)
            old_move = ()
            path_length = 1
            while flag:
                moves = self.find_available_false_moves(move)
                move, flag = self.select_false_move(moves)

                if not flag:
                    if old_move and path_length > false_path_setting:
                        self.final_invalid_moves.append(old_move)
                else:
                    old_move = move
                    path_length += 1

    def item_respawn(self):
        put_items = []
        while len(put_items) < 5:
            item_y_x = random.choice(self.final_invalid_moves)
            if self.map[item_y_x[0]][item_y_x[1]] == EXTRA_PATH and item_y_x not in put_items:
                self.map[item_y_x[0]][item_y_x[1]] = ITEM
                put_items.append(item_y_x)
                self.final_invalid_moves.remove(item_y_x)
                self.items += 1

    def convert_map(self):
        self.map = [[CELL if el == EXTRA_PATH else el for el in row] for row in self.map]

    def generate_map(self) -> None:
        self.create_empty_map()
        self.generate_start_position()
        self.generate_path()
        self.generate_false_path()
        self.item_respawn()
        self.convert_map()
        self.logger.info(f"Сгенерирована стартовая точка: row={self.start_row}, col={self.start_col}")
        self.logger.info("Генерация карты окончена")
