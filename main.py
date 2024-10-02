from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from map import Map
from player import Player

app = FastAPI()
app.mount("/static", StaticFiles(directory="front"), name="static")

main_map = Map(7, 7)
main_map.generate_map()
main_map.print_map()

main_player = Player(main_map.start_y, main_map.start_x)


@app.get("/")
async def home():
    return FileResponse("front/index.html")


@app.get("/favicon.ico")
async def main():
    return FileResponse("front/favicon.png")


@app.get("/map")
async def return_map() -> dict:
    main_player.set_player_position(main_map)
    return {"map": main_map.map}


class MoveReq(BaseModel):
    direction: str


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    try:
        game_map, completed = main_player.set_player_position(main_map, move.direction, response)

        if completed:
            return {"map": game_map, "complete": 1}
        else:
            return {"map": game_map}
    except TypeError:
        pass
