import random

from logger import Logger


class Map:

    def __init__(self, rows: int, columns: int, logger: Logger):
        self.columns = columns
        self.rows = rows
        self.min_row = 0
        self.max_row = None
        self.min_column = 0
        self.max_column = None
        self.y = None
        self.x = None
        self.map = None
        self.final = tuple()
        self.final_invalid_moves = []
        self.start_y = None
        self.start_x = None
        self.completed = False
        self.logger = logger.logger
        self.logger.info("Экземпляр карты создан")
        self.logger.info(f"Размеры карты rows={self.rows}, columns={self.columns}")

    def create_empty_map(self) -> None:
        self.map = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def print_map(self) -> None:
        for n, row in enumerate(self.map):
            print(f"Row {n}: {row}")
        print("\n")

    def generate_start_position(self) -> None:
        self.max_row = len(self.map) - 1
        self.max_column = len(self.map[0]) - 1

        self.start_y = self.y = random.randint(self.min_row, self.max_row)
        self.start_x = self.x = random.randint(self.min_column, self.max_column)

        if self.y != self.min_row or self.y != self.max_row:
            self.start_x = self.x = random.choice([self.min_column, self.max_column])

    def generate_path(self) -> None:
        self.map[self.y][self.x] = 1
        path_length = 0
        while path_length < 200:
            loop_flag = True
            while loop_flag:
                path_length += 1
                moves = self.find_available_moves()
                loop_flag = self.select_move(moves)

                if loop_flag is False and path_length < 200:
                    path_length = 0
                    self.create_empty_map()
                    self.generate_start_position()
                    self.map[self.y][self.x] = 1

    def find_available_moves(self) -> list[tuple]:
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.map[self.y + check[0]][self.x + check[1]] == 0:
                    if (self.y + check[0]) != -1 and (self.x + check[1]) != -1:
                        available_moves.append((self.y + check[0], self.x + check[1]))
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
                        if self.map[new_y][new_x] == 1:
                            score += 1

                if score <= 2:

                    if move not in final_moves:
                        final_moves.append(move)
        except IndexError:
            pass
        if final_moves:
            move = random.choice(final_moves)
            self.y, self.x = move
            self.map[self.y][self.x] = 1
            return True
        else:
            self.map[self.y][self.x] = 3
            self.final = (self.y, self.x)
            return False

    def find_right_positions(self):
        false_positions = []
        for row in self.map:
            zero_indices = [index for index, element in enumerate(row) if element == 1 or element == 3]
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
                if self.map[y + check[0]][x + check[1]] == 0:
                    if (y + check[0]) != -1 and (x + check[1]) != -1:
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
                # print("move for score", move)
                score = 0
                for check in check_tuples:
                    new_y = move[0] + check[0]
                    new_x = move[1] + check[1]
                    if 0 <= new_y < self.max_row + 1 and 0 <= new_x < self.max_column + 1:
                        if self.map[new_y][new_x] == 1 or self.map[new_y][new_x] == 4:
                            score += 1
                # print("score", score)

                if score <= 2:
                    final_moves.append(move)

        except IndexError:
            pass

        if final_moves:
            move = random.choice(final_moves)
            self.map[move[0]][move[1]] = 4
            return move, True
        else:
            return final_moves, False

    def generate_false_path(self):
        right_positions = self.find_right_positions()
        for position in right_positions:
            moves = self.find_available_false_moves(position)
            move, flag = self.select_false_move(moves)
            old_move = ()
            path_lenght = 1
            while flag:
                moves = self.find_available_false_moves(move)
                move, flag = self.select_false_move(moves)

                if not flag:
                    if old_move and path_lenght > 4:
                        self.final_invalid_moves.append(old_move)
                else:
                    old_move = move
                    path_lenght += 1

    def item_respawn(self):
        i = 0
        while i < 5:
            item_y_x = random.choice(self.final_invalid_moves)

            if self.map[item_y_x[0]][item_y_x[1]] == 4:
                self.map[item_y_x[0]][item_y_x[1]] = 5
                i += 1

    def convert_map(self):
        self.map = [[1 if el == 4 else el for el in row] for row in self.map]

    def generate_map(self) -> None:
        self.create_empty_map()
        self.generate_start_position()
        self.generate_path()
        self.generate_false_path()
        self.item_respawn()
        self.convert_map()
        self.logger.info(f"Сгенерирована стартовая точка: row={self.start_y}, col={self.start_x}")
        self.logger.info("Генерация карты окончена")
