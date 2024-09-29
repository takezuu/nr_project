import random


def print_map(map_i):
    n = 0
    for i in map_i:
        print(f"Row {n}", i)
        n += 1
    print("\n")


def create_empty_map(elements, rows):
    return [[0 for i in range(elements)] for i in range(rows)]


def random_start_position(map_i):
    min_row, min_el = 0, 0
    max_row = len(map_i) - 1
    max_el = len(map_i[0]) - 1

    y = random.randint(min_row, max_row)
    x = random.randint(min_el, max_el)

    if y != min_row or y != max_row:
        x = random.choice([min_el, max_el])

    return y, x


def generate_path(map_i, begin_y, begin_x):
    last_y_x = None
    map_i[begin_y][begin_x] = 1
    moves = find_available_moves(map_i, begin_y, begin_x)
    new_y_x = select_move(map_i, moves)
    map_i[new_y_x[0]][new_y_x[1]] = 1

    while True:
        moves = find_available_moves(map_i, new_y_x[0], new_y_x[1])
        if len(moves) == 0:
            break
        last_y_x = new_y_x
        new_y_x = select_move(map_i, moves)
        try:
            map_i[new_y_x[0]][new_y_x[1]] = 1
        except TypeError:
            map_i[last_y_x[0]][last_y_x[1]] = 3
            break

    return map_i, last_y_x


def find_available_moves(map_i, old_y, old_x):
    available_moves = []
    check_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    # [(0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    move = 0
    for ch_tuple in check_list:
        try:
            if map_i[old_y + ch_tuple[0]][old_x + ch_tuple[1]] == 0 or map_i[old_y + ch_tuple[0]][
                old_x + ch_tuple[1]] != 1:
                if (old_y + ch_tuple[0]) != -1 and (old_x + ch_tuple[1]) != -1:
                    available_moves.append((old_y + ch_tuple[0], old_x + ch_tuple[1]))
                    move += 1
        except IndexError:
            move += 1
            pass
    return available_moves


def select_move(map_i, moves):
    rows = len(map_i)
    cols = len(map_i[0])
    check_list = [(0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    final_moves = []
    try:
        for move in moves:
            score = 0
            for check in check_list:
                new_y = move[0] + check[0]
                new_x = move[1] + check[1]
                if 0 <= new_y < rows and 0 <= new_x < cols:
                    if map_i[new_y][new_x] == 1:
                        score += 1

            if score <= 2:
                if move not in final_moves:
                    final_moves.append(move)
    except IndexError:
        pass

    if final_moves:
        move = random.choice(final_moves)
        return move




def create_map(rows, columns):
    empty_map = (create_empty_map(columns, rows))
    path_y, path_x = random_start_position(empty_map)
    game_map, final = generate_path(empty_map, path_y, path_x)
    return game_map, final, path_y, path_x
