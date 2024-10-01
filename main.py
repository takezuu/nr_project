from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from fastapi import status
from algo import create_map, print_map

app = FastAPI()

app.mount("/static", StaticFiles(directory="front"), name="static")

main_map, final, begin_y, begin_x = create_map(10, 10)
player_position = {"y": begin_y,
                   "x": begin_x}

print_map(main_map)


def set_begin_player_position(p_position, map_i):
    map_i[p_position["y"]][p_position["x"]] = 2
    return map_i


def set_player_position(map_i, final_i, direction, p_position, response):
    global player_position
    x, y = 0, 0
    if direction == "right":
        x = 1
    elif direction == "left":
        x = -1
    elif direction == "up":
        y = -1
    elif direction == "down":
        y = 1

    if map_i[p_position["y"] + y][p_position["x"] + x] != 0:
        map_i[p_position["y"]][p_position["x"]] = 1
        player_position["x"] += x
        player_position["y"] += y
        map_i[p_position["y"]][p_position["x"]] = 2

        if player_position["y"] == final_i[0] and player_position["x"] == final_i[1]:
            return map_i, True
        else:
            return map_i, False

    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


@app.get("/")
async def home():
    return FileResponse("front/index.html")


@app.get("/map")
async def return_map():
    game_map = set_begin_player_position(player_position, main_map)
    return {"map": game_map}


@app.get("/favicon.ico")
async def main():
    return FileResponse("front/favicon.png")


class MoveReq(BaseModel):
    direction: str


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    game_map, completed = set_player_position(main_map, final, move.direction, player_position, response)

    if completed:
        return {"map": game_map, "complete": 1}
    else:
        return {"map": game_map}
