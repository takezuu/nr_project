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

player = Player(main_map.start_y, main_map.start_x)


def set_begin_player_position(p_position, map_i):
    map_i[p_position.y][p_position.x] = 2
    return map_i


def set_player_position(map_i, final_i, direction, p_position, response):
    global player, main_map
    x, y = 0, 0

    match direction:
        case "right":
            x = 1
        case "left":
            x = -1
        case "up":
            y = -1
        case "down":
            y = 1

    try:
        if map_i[p_position.y + y][p_position.x + x] != 0:
            if p_position.y + y != -1 and p_position.x + x != -1:

                map_i[p_position.y][p_position.x] = 1
                player.y += y
                player.x += x
                map_i[p_position.y][p_position.x] = 2

                if player.y == final_i[0] and player.x == final_i[1]:
                    return map_i, True
                else:
                    return map_i, False

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
    game_map = set_begin_player_position(player, main_map.map)
    return {"map": game_map}


@app.get("/favicon.ico")
async def main():
    return FileResponse("front/favicon.png")


class MoveReq(BaseModel):
    direction: str


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    try:
        game_map, completed = set_player_position(main_map.map, main_map.final, move.direction, player, response)

        if completed:
            return {"map": game_map, "complete": 1}
        else:
            return {"map": game_map}
    except TypeError:
        pass
