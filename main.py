from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import chess
import chess.engine
from typing import Optional
import subprocess


class MoveInput(BaseModel):
    fen: str
    time: Optional[float]
    depth: Optional[int]


class MoveResult(MoveInput):
    best_move: str
    w_score: Optional[int]
    b_score: Optional[int]
    pv: list[str]
    nodes: int


log_instance = logging.getLogger("fastapi")
log_instance.setLevel(logging.DEBUG)


def log(log: str):
    log_instance.error(log)


# Mute the engine logs with stderr=subprocess.DEVNULL
engine = chess.engine.SimpleEngine.popen_uci(
    "engine/chesso_engine", stderr=subprocess.DEVNULL)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/make_move", response_model=MoveResult)
async def post_make_move(board_status: MoveInput):

    # log(board_status)

    board = chess.Board(board_status.fen)

    play_result = None
    if board_status.time > 0:
        play_result = engine.play(
            board, chess.engine.Limit(time=board_status.time), info=chess.engine.INFO_ALL)

    if board_status.depth > 0:
        play_result = engine.play(
            board, chess.engine.Limit(depth=board_status.depth), info=chess.engine.INFO_ALL)

    if board_status.depth == 0 and board_status.time == 0:
        play_result = engine.play(
            board, chess.engine.Limit(time=0.01), info=chess.engine.INFO_ALL)

    if not play_result:
        raise HTTPException(
            status_code=500, detail="Failed to execute the engine")

    best_move = play_result.move
    info = play_result.info

    board.push(best_move)
    fen = board.fen()

    pv = []
    if info:
        pv = [str(move) for move in info['pv']]

    w_score = 0
    b_score = 0
    if info:
        score = info['score']
        w_score = score.white().score()
        b_score = score.black().score()

    nodes = 0
    if info:
        nodes = info['nodes']

    time = 0
    if info:
        time = info['time']

    depth = 0
    if info:
        depth = info['depth']

    result = MoveResult(
        fen=fen,
        best_move=str(best_move),
        w_score=w_score,
        b_score=b_score,
        pv=pv,
        nodes=nodes,
        time=time,
        depth=depth)

    return result


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
