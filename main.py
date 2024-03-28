from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/make-move", response_model=str)
async def post_make_move(fen: str):
    return fen


# @app.get("/img/chesspieces/wikipedia/{image}")
# async def get_chesspieces():
    


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
