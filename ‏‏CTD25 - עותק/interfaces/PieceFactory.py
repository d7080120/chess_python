# # # import pathlib
# # # from typing import Dict, Tuple
# # # import json
# # # from Board import Board
# # # from GraphicsFactory import GraphicsFactory
# # # from Moves import Moves
# # # from PhysicsFactory import PhysicsFactory
# # # from Piece import Piece
# # # from State import State


# # # class PieceFactory:
# # #     def __init__(self, board: Board, pieces_root: pathlib.Path):
# # #         """Initialize piece factory with board and 
# # #         generates the library of piece templates from the pieces directory.."""
# # #         pass

# # #     def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
# # #         """Build a state machine for a piece from its directory."""
# # #         pass

# # #     # PieceFactory.py  – replace create_piece(...)
# # #     def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
# # #         """Create a piece of the specified type at the given cell."""
# # #         pass 


# # import pathlib
# # from typing import Dict, Tuple
# # import json
# # from .Board import Board
# # from .GraphicsFactory import GraphicsFactory
# # from .Moves import Moves
# # from .PhysicsFactory import PhysicsFactory
# # from .Piece import Piece
# # from .State import State

# # class PieceFactory:
# #     def __init__(self, board: Board, pieces_root: pathlib.Path):
# #         """Initialize piece factory with board and pieces root directory."""
# #         self.board = board
# #         self.pieces_root = pieces_root
# #         self.graphics_factory = GraphicsFactory()
# #         self.physics_factory = PhysicsFactory(board)
# #         self.cache: Dict[str, dict] = {}

# #     def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
# #         """Build a state machine for a piece from its directory."""
# #         # טוען את הקובץ JSON
# #         cfg_path = piece_dir / "state.json"
# #         with open(cfg_path, 'r') as f:
# #             cfg = json.load(f)

# #         # הגדרת רכיבים
# #         sprites_dir = piece_dir / "states" / "idle" / "sprites"
# #         graphics = self.graphics_factory.load(
# #             sprites_dir=sprites_dir,
# #             cfg=cfg.get("graphics", {}),
# #             cell_size=(self.board.cell_W_pix, self.board.cell_H_pix)
# #         )

# #         moves_path = piece_dir / "moves.txt"
# #         moves = Moves(moves_path, dims=(self.board.H_cells, self.board.W_cells))

# #         physics = self.physics_factory.create((0, 0), cfg.get("physics", {}))

# #         return State(moves, graphics, physics)

# #     def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
# #         """Create a piece of the specified type at the given cell."""
# #         piece_dir = self.pieces_root / p_type
# #         state = self._build_state_machine(piece_dir)
# #         physics = state._physics
# #         physics.reset(Command(timestamp=0, piece_id="none", type="idle", params=[cell]))  # הגדרת מיקום

# #         return Piece(piece_id=p_type, init_state=state)


# import pathlib
# from typing import Dict, Tuple
# import json
# from .Board import Board
# from .GraphicsFactory import GraphicsFactory
# from .Moves import Moves
# from .PhysicsFactory import PhysicsFactory
# from .Piece import Piece
# from .State import State
# from .Command import Command


# class PieceFactory:
#     def __init__(self, board: Board, pieces_root: pathlib.Path):
#         """Initialize piece factory with board and root pieces path."""
#         self.board = board
#         self.pieces_root = pieces_root
#         self.graphics_factory = GraphicsFactory()
#         self.physics_factory = PhysicsFactory(board)

#     def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
#         """Build the initial state of a piece using the RB layout."""
#         state_dir = piece_dir / "states" / "idle"
#         sprites_dir = state_dir / "sprites"
#         cfg_path = state_dir / "config.json"

#         if not cfg_path.exists():
#             raise FileNotFoundError(f"Missing config.json in {cfg_path}")

#         with open(cfg_path, "r") as f:
#             cfg = json.load(f)

#         # Load moves
#         moves_path = piece_dir / "moves.txt"
#         moves = Moves(moves_path, dims=(self.board.H_cells, self.board.W_cells))

#         # Load graphics
#         graphics = self.graphics_factory.load(
#             sprites_dir=sprites_dir,
#             cfg=cfg.get("graphics", {}),
#             cell_size=(self.board.cell_W_pix, self.board.cell_H_pix)
#         )

#         # Load physics
#         physics = self.physics_factory.create(start_cell=(0, 0), cfg=cfg.get("physics", {}))

#         return State(moves, graphics, physics)

#     def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
#         """Instantiate a piece from a given type and cell."""
#         piece_dir = self.pieces_root / p_type
#         state = self._build_state_machine(piece_dir)

#         # Set start position
#         cmd = Command(timestamp=0, piece_id=p_type, type="idle", params=[cell])
#         state._physics.reset(cmd)

#         return Piece(piece_id=p_type, init_state=state)


import pathlib
import json
from typing import Dict, Tuple
from .Board import Board
from .GraphicsFactory import GraphicsFactory
from .Moves import Moves
from .PhysicsFactory import PhysicsFactory
from .Piece import Piece
from .State import State
from .Command import Command


class PieceFactory:
    def __init__(self, board: Board, pieces_root: pathlib.Path):
        self.board = board
        self.pieces_root = pieces_root
        self.graphics_factory = GraphicsFactory()
        self.physics_factory = PhysicsFactory(board)

    def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
        moves_path = piece_dir / "moves.txt"
        moves = Moves(moves_path, dims=(self.board.H_cells, self.board.W_cells))

        states_root = piece_dir / "states"
        states: Dict[str, State] = {}

        # שלב א: צור אובייקטי סטייטים
        for state_dir in states_root.iterdir():
            if not state_dir.is_dir():
                continue
            state_name = state_dir.name
            cfg_path = state_dir / "config.json"
            sprites_dir = state_dir / "sprites"

            with open(cfg_path, 'r') as f:
                cfg = json.load(f)

            graphics = self.graphics_factory.load(
                sprites_dir=sprites_dir,
                cfg=cfg.get("graphics", {}),
                cell_size=(self.board.cell_W_pix, self.board.cell_H_pix)
            )
            physics = self.physics_factory.create((0, 0), cfg.get("physics", {}))

            states[state_name] = State(moves, graphics, physics)

        # שלב ב: הגדרת מעברים לפי config.json
        for state_name, state in states.items():
            cfg_path = states_root / state_name / "config.json"
            with open(cfg_path, 'r') as f:
                cfg = json.load(f)
            next_state = cfg.get("physics", {}).get("next_state_when_finished")
            if next_state and next_state in states:
                state.set_transition("finished", states[next_state])

        return states["idle"]

    def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
        piece_dir = self.pieces_root / p_type
        init_state = self._build_state_machine(piece_dir)

        init_cmd = Command(timestamp=0, piece_id=p_type, type="idle", params=[cell])
        init_state._physics.reset(init_cmd)

        return Piece(piece_id=p_type, init_state=init_state)
