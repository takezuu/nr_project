from typing import Union, Tuple

from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from fastapi import status
from map import Map
from player import Player

app = FastAPI()

app.mount("/static", StaticFiles(directory="front"), name="static")

main_map = Map(7, 7)
main_map.generate_map()
main_map.print_map()

main_player = Player(main_map.start_y, main_map.start_x)


def set_player_position(game_map: Map, player: Player, direction: str = None, response: Response = None):
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
        if game_map[player.y + y][player.x + x] != 0:
            if player.y + y != -1 and player.x + x != -1:

                game_map[player.y][player.x] = 1
                player.y += y
                player.x += x
                game_map[player.y][player.x] = 2

                if player.y == final[0] and player.x == final[1]:
                    return game_map, True
                else:
                    return game_map, False

        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return response
    except IndexError:
        pass


@app.get("/")
async def home():
    return FileResponse("front/index.html")


@app.get("/map")
async def return_map():
    set_player_position(main_map, main_player)
    return {"map": main_map.map}


@app.get("/favicon.ico")
async def main():
    return FileResponse("front/favicon.png")


class MoveReq(BaseModel):
    direction: str


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    try:
        game_map, completed = set_player_position(main_map, main_player, move.direction, response)

        if completed:
            return {"map": game_map, "complete": 1}
        else:
            return {"map": game_map}
    except TypeError:
        pass
