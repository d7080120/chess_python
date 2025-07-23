
import numpy as np
from interfaces.Graphics import Graphics
from interfaces.Board import Board
from interfaces.mock_img import MockImg  # אנחנו משתמשים ב- MockImg במקום Img בטסטים
from interfaces.Command import Command
from interfaces.img import Img
import pathlib

def test_load_sprites():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=MockImg())  
    sprites_folder = pathlib.Path("CTD25/pieces/RB/states/idle/sprites")
    graphics = Graphics(sprites_folder, board)
    assert len(graphics.sprites) > 0

def test_graphics_copy():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=MockImg())  
    sprites_folder = pathlib.Path("CTD25/pieces/RB/states/idle/sprites")
    graphics = Graphics(sprites_folder, board)
    copied_graphics = graphics.copy()
    assert len(copied_graphics.sprites) == len(graphics.sprites)
    for i in range(len(graphics.sprites)):
        assert np.array_equal(copied_graphics.sprites[i].img, graphics.sprites[i].img)

def test_graphics_reset():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=MockImg())  
    sprites_folder = pathlib.Path("CTD25/pieces/RB/states/idle/sprites")
    graphics = Graphics(sprites_folder, board)
    cmd = Command(timestamp=0, piece_id="g1", type="move", params=[(0, 0), (1, 2)])
    graphics.reset(cmd)
    assert isinstance(graphics.get_img(), Img)

def test_sprites_length():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=MockImg())  
    sprites_folder = pathlib.Path("CTD25/pieces/RB/states/idle/sprites")
    graphics = Graphics(sprites_folder, board)
    assert len(graphics.sprites) > 0

def test_current_frame():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=MockImg())  
    sprites_folder = pathlib.Path("CTD25/pieces/RB/states/idle/sprites")
    graphics = Graphics(sprites_folder, board)
    initial_frame = graphics.get_img()
    cmd = Command(timestamp=0, piece_id="g1", type="move", params=[(0, 0), (1, 2)])
    graphics.reset(cmd)
    assert initial_frame != graphics.get_img()
