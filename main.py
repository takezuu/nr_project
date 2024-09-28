from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from fastapi import status

app = FastAPI()

app.mount("/static", StaticFiles(directory="front"), name="static")

player_position = {"y": 2,
                   "x": 2}

main_map = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

zero_main_map = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

def generate_map():
    zero_main_map[0][0] = 1


def set_begin_player_position(p_position, map_i):
    map_i[p_position["y"]][p_position["x"]] = 2
    return map_i


def set_player_position(map_i, direction, p_position, response):
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
        return map_i

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
    game_map = set_player_position(main_map, move.direction, player_position, response)
    return {"map": game_map}
