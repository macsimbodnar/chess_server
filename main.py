from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import asyncio
import chess
import chess.engine


class FEN(BaseModel):
    fen: str


log_instance = logging.getLogger("fastapi")
log_instance.setLevel(logging.DEBUG)


def log(log: str):
    log_instance.error(log)


engine = chess.engine.SimpleEngine.popen_uci(
    "/home/max/Downloads/Software/stockfish-ubuntu-x86-64-avx2/stockfish/stockfish-ubuntu-x86-64-avx2")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/make_move", response_model=FEN)
async def post_make_move(fen: FEN):
    board = chess.Board(fen.fen)
    move = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(move.move)

    result = FEN(fen=board.fen())
    return result


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
