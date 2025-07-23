import pathlib
import json
from interfaces.Board import Board
from interfaces.PieceFactory import PieceFactory
from interfaces.Piece import Piece
from interfaces.mock_img import MockImg
from interfaces import img  # ← נדרש עבור monkeypatch

def test_create_piece_returns_piece_object(tmp_path, monkeypatch):
    # שנה את Img ל-MockImg בכל המודולים
    monkeypatch.setattr(img.Img, "read", lambda self, path, *a, **kw: self)

    piece_name = "BB"
    piece_dir = tmp_path / piece_name
    sprites_dir = piece_dir / "states" / "idle" / "sprites"
    sprites_dir.mkdir(parents=True)

    config = {
        "physics": {
            "speed_m_per_sec": 0.0,
            "next_state_when_finished": "idle"
        },
        "graphics": {
            "frames_per_sec": 6,
            "is_loop": True
        }
    }
    (piece_dir / "states" / "idle" / "config.json").write_text(json.dumps(config))
    (piece_dir / "moves.txt").write_text("1,0\n0,1")

    for i in range(1, 4):
        (sprites_dir / f"{i}.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    board = Board(
        cell_H_pix=64,
        cell_W_pix=64,
        cell_H_m=1,
        cell_W_m=1,
        W_cells=8,
        H_cells=8,
        img=MockImg()
    )
    factory = PieceFactory(board, tmp_path)
    piece = factory.create_piece(piece_name, (3, 5))

    assert isinstance(piece, Piece)
    assert piece._state is not None
