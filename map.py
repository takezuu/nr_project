import random


class Map:

    def __init__(self, rows: int, columns: int):
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
        self.start_y = None
        self.start_x = None

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
        while path_length < 500000:
            loop_flag = True
            while loop_flag:
                path_length += 1
                moves = self.find_available_moves()
                loop_flag = self.select_move(moves)

                if loop_flag is False and path_length < 500000:
                    path_length = 0
                    self.create_empty_map()
                    self.generate_start_position()
                    self.map[self.y][self.x] = 1

    def find_available_moves(self) -> list[tuple]:
        available_moves = []
        check_tuples = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # координаты для расчета доступных ходов
        for check in check_tuples:
            try:
                if self.map[self.y + check[0]][self.x + check[1]] == 0 or self.map[self.y + check[0]][
                    self.x + check[1]] != 1:
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
                        if self.map[new_y][new_x] == 1 or (new_y - 1 == self.start_y and new_x - 1 == self.start_x) or \
                                (new_y + 1 == self.start_y and new_x + 1 == self.start_x) or \
                                (new_y + 1 == self.start_y and new_x + 0 == self.start_x) or \
                                (new_y + 0 == self.start_y and new_x + 1 == self.start_x) or \
                                (new_y - 1 == self.start_y and new_x + 0 == self.start_x) or \
                                (new_y - 0 == self.start_y and new_x + 1 == self.start_x):
                            score += 1

                if score <= 2:

                    if move not in final_moves:
                        final_moves.append(move)
        except IndexError:
            pass
        if final_moves:
            move = random.choice(final_moves)
            self.y = move[0]
            self.x = move[1]
            self.map[self.y][self.x] = 1
            return True
        else:
            self.map[self.y][self.x] = 3
            self.final = (self.y, self.x)
            return False

    def generate_map(self) -> None:
        self.create_empty_map()
        self.generate_start_position()
        self.generate_path()
