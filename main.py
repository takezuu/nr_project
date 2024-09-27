from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

app.mount("/", StaticFiles(directory="front", html=True), name="front")


class MoveReq(BaseModel):
    direction: str
    cellNum: int


@app.post("/move")
async def move(move: MoveReq):
    if move.direction == "right" and move.cellNum + 1 > move.cellNum:
        return {"Message": f"You can move cellNum = {move.cellNum + 1}"}
    else:
        return {"Status": 500, "Message": "Wrong move"}
