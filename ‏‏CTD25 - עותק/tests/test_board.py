import pytest  # אם אתה משתמש ב-pytest לניהול הטסטים
from interfaces.Board import Board
from interfaces.mock_img import MockImg
from interfaces.img import Img

def test_board_clone():
    img = MockImg()  # נשתמש ב- MockImg לצורך הבדיקות
    board = Board(
        cell_H_pix=100, cell_W_pix=100, 
        cell_H_m=1, cell_W_m=1,
        W_cells=8, H_cells=8,
        img=img
    )

    # Clone the board
    cloned_board = board.clone()

    # ודא שהעתקת הלוח הושלמה בהצלחה
    assert cloned_board.cell_H_pix == board.cell_H_pix
    assert cloned_board.cell_W_pix == board.cell_W_pix
    assert cloned_board.cell_H_m == board.cell_H_m
    assert cloned_board.cell_W_m == board.cell_W_m
    assert cloned_board.W_cells == board.W_cells
    assert cloned_board.H_cells == board.H_cells

    # ודא שהתמונה הועתקה (העתק של התמונה ולא הפניה לאותו אובייקט)
    assert cloned_board.img is not board.img
    assert cloned_board.img.img == board.img.img  # מבצעים השוואה על תמונת ה-MockImg

def test_board_get_cell_dimensions():
    img = MockImg()
    board = Board(
        cell_H_pix=100, cell_W_pix=100, 
        cell_H_m=1, cell_W_m=1,
        W_cells=8, H_cells=8,
        img=img
    )
    h, w = board.get_cell_dimensions()
    assert h == 100
    assert w == 100

def test_board_get_board_size_in_meters():
    img = MockImg()
    board = Board(
        cell_H_pix=100, cell_W_pix=100, 
        cell_H_m=1, cell_W_m=1,
        W_cells=8, H_cells=8,
        img=img
    )
    h, w = board.get_board_size_in_meters()
    assert h == 8
    assert w == 8

def test_board_draw():
    img = MockImg()
    board = Board(
        cell_H_pix=100, cell_W_pix=100,
        cell_H_m=1, cell_W_m=1,
        W_cells=8, H_cells=8,
        img=img
    )
    
    other_img = MockImg()  # התמונה שאליה נצייר
    board.draw(other_img, 10, 10)  # צייר בלוק (10,10)

    # נוודא שזכור לנו היכן התמונה הוצבה
    assert (10, 10) in MockImg.traj
