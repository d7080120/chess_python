import pathlib
from .Game import Game
from .Board import Board
from .Piece import Piece
from .Moves import Moves
from .State import State
from .GraphicsFactory import GraphicsFactory
from .PhysicsFactory import PhysicsFactory
from .Command import Command
from .PieceFactory import PieceFactory
from .img import Img  # ייבוא הכרחי

import json

def read_config(path):
    with open(path, "r") as f:
        return json.load(f)

def read_board(path: pathlib.Path) -> list[tuple[str, tuple[int, int]]]:
    with open(path) as f:
        lines = [line.strip().split(",") for line in f if line.strip()]

    board_data = []
    for row_idx, row in enumerate(lines):
        for col_idx, cell in enumerate(row):
            if cell:
                board_data.append((cell.strip(), (col_idx, row_idx))) 
    return board_data

def create_piece(piece_id: str, location: tuple[int, int], root_folder: pathlib.Path, board: Board) -> Piece:
    folder = root_folder / piece_id
    moves = Moves(folder / "moves.txt", (board.H_cells, board.W_cells))
    states = {}
    states_folder = folder / "states"
    for subfolder in states_folder.iterdir():
        state_name = subfolder.name
        cfg_path = subfolder / "config.json"
        cfg = read_config(cfg_path)

        physics = PhysicsFactory(board).create(location, cfg["physics"])
        graphics = GraphicsFactory().load(subfolder / "sprites", cfg["graphics"], (board.cell_W_pix, board.cell_H_pix))

        states[state_name] = State(moves, graphics, physics)

    # Transitions
    states["idle"].set_transition("move", states["move"])
    states["idle"].set_transition("jump", states["jump"])
    states["move"].set_transition("long_rest", states["long_rest"])
    states["jump"].set_transition("short_rest", states["short_rest"])
    states["long_rest"].set_transition("idle", states["idle"])
    states["short_rest"].set_transition("idle", states["idle"])

    cmd = Command(piece_id=piece_id, type="idle", params=[location, location], timestamp=0)
    states["idle"].reset(cmd)
    states["idle"].update(0)
    return Piece(piece_id, states["idle"])

def clone_piece(template_piece: Piece, location: tuple[int, int]) -> Piece:
        state_copy = template_piece._state.copy()  # יצירת עותק של ה־State
        cmd = Command(piece_id=template_piece._piece_id, type="idle", params=[location, location], timestamp=0)
        state_copy.reset(cmd)
        state_copy.update(0)
        return Piece(template_piece._piece_id, state_copy)

def create_game(board_txt_path: pathlib.Path, root_folder: pathlib.Path) -> Game:
    img = Img().read("board.png", size=(64 * 8, 64 * 8))  # קריאת תמונת הלוח
    board = Board(64, 64, 1, 1, 8, 8, img)  # יצירת לוח עם התמונה
    board_data = read_board(board_txt_path)
    pieces_templates = {}
    game_pieces = []

    # קריאת רקע הלוח מהתמונה
    board_img = Img().read("board.png", size=(64 * 8, 64 * 8))
    # יצירת לוח עם רקע
    board = Board(64, 64, 1, 1, 8, 8, board_img)

    for piece_id, location in board_data:
        if piece_id not in pieces_templates:
            pieces_templates[piece_id] = create_piece(piece_id, location, root_folder, board)

        p = clone_piece(pieces_templates[piece_id], location)
        game_pieces.append(p)

    return Game(game_pieces, board)


def main():
    game = create_game(pathlib.Path("pieces/board.csv"), pathlib.Path("pieces/"))
    game.run()

if __name__ == "__main__":
    main()
