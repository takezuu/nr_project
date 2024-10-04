from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from logger import Logger
from map import Map
from player import Player


class MoveReq(BaseModel):
    col: int
    row: int


app = FastAPI()
app.mount("/static", StaticFiles(directory="front2"), name="static")
logger = Logger()

main_map = Map(30, 40, logger)
main_map.generate_map()

main_player = Player(main_map.start_y, main_map.start_x, logger)


@app.get("/")
async def home():
    return FileResponse("front2/board.html")


@app.get("/favicon.ico")
async def main():
    return FileResponse("front2/favicon.png")


@app.get("/map")
async def return_map() -> dict:
    main_player.set_player_position(main_map)
    main_map.print_map()
    return {"map": main_map.map, "playerPosition": {"row": main_player.y, "col": main_player.x}}


@app.get("/remap")
async def return_new_map():
    global main_map, main_player

    if not main_map.completed:
        return "Now it's your problem go back to default URL"
    main_map.create_empty_map()
    main_map.generate_map()

    main_player.y = main_map.start_y
    main_player.x = main_map.start_x

    main_player.set_player_position(main_map)
    main_map.print_map()
    return {"map": main_map.map, "playerPosition": {"row": main_player.y, "col": main_player.x}}


@app.post("/move", status_code=200)
async def move_func(move: MoveReq):
    global main_player, main_map
    try:
        bool_move, completed = main_player.set_player_position(main_map, move)

        if completed:
            main_map.completed = True
            return {"playerPosition": {"row": main_player.y, "col": main_player.x}, "complete": 1,
                    "moveForward": bool_move}
        else:
            return {"playerPosition": {"row": main_player.y, "col": main_player.x}, "moveForward": bool_move}
    except TypeError:
        pass
