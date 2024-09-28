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
    return FileResponse("front/favicon.png")


class MoveReq(BaseModel):
    direction: str
    position: int


@app.post("/move", status_code=200)
async def move_func(move: MoveReq, response: Response):

    if move.position == 3:
        match move.direction:
            case "up":
                return {"position": 1}
            case "down":
                return {"position": 5}
            case "left":
                return {"position": 2}
            case "right":
                return {"position": 4}

    elif move.position == 1:
        if move.direction == "down":
            return {"position": 3}
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return response

    elif move.position == 2:
        if move.direction == "right":
            return {"position": 3}
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return response

    elif move.position == 4:
        if move.direction == "left":
            return {"position": 3}
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return response

    elif move.position == 5:
        if move.direction == "up":
            return {"position": 3}
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return response
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
