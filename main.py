import chess.pgn
from stockfish import Stockfish

BLUNDER_THRESHOLD = -150

sf = Stockfish(path="/home/jud/projects/sf/stockfish16.1")

pgn = open("./game.pgn")
game = chess.pgn.read_game(pgn)

board = chess.Board()

prev_cp = 30
sf.set_depth(18)

for move in game.mainline_moves():
    print(f"{board.fullmove_number:>3}{'.'*(1 if board.turn == chess.WHITE else 3):<3}", end="")
    print(f"{board.san(move):<7} ", end="")

    board.push(move)

    sf.set_fen_position(board.fen())
    sf_eval = sf.get_evaluation()

    # convert to POV eval
    to_pov = 1 if board.turn == chess.BLACK else -1

    if sf_eval["type"] == "cp":
        cp = sf_eval["value"] * to_pov
    else:
        mate = sf_eval["value"] * to_pov
        cp = 10000 if mate > 0 else -10000

    delta = prev_cp + cp
    prev_cp = cp

    print(f"{(cp*to_pov)/100.0:7.2f} ", end="")

    if delta < BLUNDER_THRESHOLD:
        print(" ??", end="")

    print()
