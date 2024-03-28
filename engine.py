import asyncio
import chess
import chess.engine
from chessboard import display
from time import sleep


async def main() -> None:
    transport, engine = await chess.engine.popen_uci("/home/max/Downloads/Software/stockfish-ubuntu-x86-64-avx2/stockfish/stockfish-ubuntu-x86-64-avx2")

    board = chess.Board()
    bb = display.start(board.fen())

    while not board.is_game_over():
        result = await engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        display.update(board.fen(), bb)
        sleep(1)


    await engine.quit()

asyncio.run(main())


# import chess
# import chess.engine
# from chessboard import display
# from time import sleep


# engine = chess.engine.SimpleEngine.popen_uci(
#     "/home/max/Downloads/Software/stockfish-ubuntu-x86-64-avx2/stockfish/stockfish-ubuntu-x86-64-avx2")

# board = chess.Board()
# display_board = display.start(board.fen())
# while not board.is_game_over():
#     result = engine.play(board, chess.engine.Limit(time=0.1))
#     board.push(result.move)
#     display.update(board.fen(), display_board)
#     sleep(1)

# engine.quit()
