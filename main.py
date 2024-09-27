from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from fastapi import status

app = FastAPI()

app.mount("/static", StaticFiles(directory="front"), name="static")


@app.get("/")
async def main():
    return FileResponse("front/index.html")

@app.get("/favicon.ico")
async def main():
    return FileResponse("front/favicon.ico")


class MoveReq(BaseModel):
    direction: str
    position: int


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):
    if move.direction == "right" and move.position < 3:
        return {"position": move.position + 1}
    elif move.direction == "left" and move.position > 1:
        return {"position": move.position - 1}
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
