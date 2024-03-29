from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import chess
import chess.engine


class MoveInput(BaseModel):
    fen: str


class MoveResult(MoveInput):
    best_move: str


log_instance = logging.getLogger("fastapi")
log_instance.setLevel(logging.DEBUG)


def log(log: str):
    log_instance.error(log)


engine = chess.engine.SimpleEngine.popen_uci(
    "/home/max/Downloads/Software/stockfish-ubuntu-x86-64-avx2/stockfish/stockfish-ubuntu-x86-64-avx2")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/make_move", response_model=MoveResult)
async def post_make_move(board_status: MoveInput):
    board = chess.Board(board_status.fen)
    move = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(move.move)

    result = MoveResult(fen=board.fen(), best_move=str(move.move))
    return result


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
