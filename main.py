from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import chess
import chess.engine
from typing import Optional


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


engine = chess.engine.SimpleEngine.popen_uci("engine/chesso_engine_0.1.2")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/make_move", response_model=MoveResult)
async def post_make_move(board_status: MoveInput):

    # log(board_status)

    board = chess.Board(board_status.fen)

    info = None
    if board_status.time > 0:
        info = engine.analyse(
            board, chess.engine.Limit(time=board_status.time))

    if board_status.depth > 0:
        info = engine.analyse(
            board, chess.engine.Limit(depth=board_status.depth))

    if board_status.depth == 0 and board_status.time == 0:
        info = engine.analyse(
            board, chess.engine.Limit(time=0.01))

    if not info:
        raise HTTPException(
            status_code=500, detail="Failed to execute the engine")

    # PV is Principal variation
    best_move = info['pv'][0]

    board.push(best_move)
    fen = board.fen()

    pv = [str(move) for move in info['pv']]
    score = info['score']

    result = MoveResult(
        fen=fen,
        best_move=str(best_move),
        w_score=score.white().score(),
        b_score=score.black().score(),
        pv=pv,
        nodes=info['nodes'],
        time=info['time'],
        depth=info['depth'])

    return result


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
