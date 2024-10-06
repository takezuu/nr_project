from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from game import Game
from map_config import rows_setting, columns_setting


class MoveReq(BaseModel):
    col: int
    row: int


app = FastAPI()
app.mount("/static", StaticFiles(directory="front2"), name="static")
game = Game(rows_setting, columns_setting)


@app.get("/")
async def home():
    return FileResponse("front2/board.html")


@app.get("/favicon.ico")
async def main():
    return FileResponse("front2/favicon.png")


@app.get("/map")
async def return_map() -> dict:
    game.player.set_player_position(game.map)
    return {"map": game.map.map, "playerPosition": {"row": game.player.y, "col": game.player.x}}


@app.get("/remap")
async def return_new_map():
    if not game.map.completed:
        raise HTTPException(status_code=400, detail="Game not yet completed. Please finish the current game first.")
    game.map.completed = False
    game.reset()

    game.player.set_player_position(game.map)
    return {"map": game.map.map, "playerPosition": {"row": game.player.y, "col": game.player.x}}


@app.post("/move", status_code=200)
async def move_func(move: MoveReq):
    try:
        bool_move, completed = game.player.set_player_position(game.map, move)
        if completed:
            game.map.completed = True
            return {"playerPosition": {"row": game.player.y, "col": game.player.x}, "complete": 1,
                    "moveForward": bool_move}
        else:
            return {"playerPosition": {"row": game.player.y, "col": game.player.x}, "moveForward": bool_move}
    except TypeError:
        raise HTTPException(status_code=400, detail="Invalid move data.")
