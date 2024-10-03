from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from map import Map
from player import Player

app = FastAPI()
app.mount("/static", StaticFiles(directory="front2"), name="static")

main_map = Map(10, 10)
main_map.generate_map()

main_player = Player(main_map.start_y, main_map.start_x)


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
    return {"map": main_map.map, "playerPosition": {"y": main_player.y, "x": main_player.x}}


class MoveReq(BaseModel):
    playerPosition: dict


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    try:
        bool_move, completed = main_player.set_player_position(main_map, move.playerPosition, response)

        if completed:
            return {"playerPosition": {"y": main_player.y, "x": main_player.x}, "complete": 1, "moveForward": bool_move}
        else:
            return {"playerPosition": {"y": main_player.y, "x": main_player.x}, "moveForward": bool_move}
    except TypeError:
        pass
