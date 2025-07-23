import pathlib
from interfaces.GraphicsFactory import GraphicsFactory
from interfaces.Graphics import Graphics
from interfaces.mock_img import MockImg

def test_factory_creates_graphics_with_defaults():
    factory = GraphicsFactory()
    path = pathlib.Path("CTD25/pieces/BB/states/idle/sprites")
    cfg = {}  # בלי הגדרות מיוחדות
    cell_size = (100, 100)

    graphics = factory.load(path, cfg, cell_size)

    assert isinstance(graphics, Graphics)
    assert graphics.fps == 6.0
    assert graphics.loop is True
    assert len(graphics.sprites) > 0

def test_factory_respects_config():
    factory = GraphicsFactory()
    path = pathlib.Path("CTD25/pieces/BB/states/idle/sprites")
    cfg = {
        "loop": False,
        "fps": 12.0,
        "img": MockImg()
    }
    cell_size = (80, 80)

    graphics = factory.load(path, cfg, cell_size)

    assert isinstance(graphics, Graphics)
    assert graphics.fps == 12.0
    assert graphics.loop is False
    assert len(graphics.sprites) > 0

def test_factory_creates_correct_board_dimensions():
    factory = GraphicsFactory()
    path = pathlib.Path("CTD25/pieces/BB/states/idle/sprites")
    cell_size = (64, 64)
    graphics = factory.load(path, {}, cell_size)

    board = graphics.board
    assert board.cell_W_pix == 64
    assert board.cell_H_pix == 64
    assert board.W_cells == 8
    assert board.H_cells == 8
