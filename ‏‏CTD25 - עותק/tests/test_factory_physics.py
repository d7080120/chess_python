import pytest
from interfaces.PhysicsFactory import PhysicsFactory
from interfaces.Board import Board
from interfaces.Physics import Physics

def test_physics_factory_create_basic():
    board = Board(cell_H_pix=100, cell_W_pix=100,
                  cell_H_m=1, cell_W_m=1,
                  W_cells=8, H_cells=8,
                  img=None)
    factory = PhysicsFactory(board)
    cfg = {"speed": 2.5}
    start = (3, 4)
    physics = factory.create(start, cfg)

    assert isinstance(physics, Physics)
    assert physics.get_pos() == start

def test_physics_factory_default_speed():
    board = Board(cell_H_pix=100, cell_W_pix=100,
                  cell_H_m=1, cell_W_m=1,
                  W_cells=8, H_cells=8,
                  img=None)
    factory = PhysicsFactory(board)
    physics = factory.create((0, 0), {})  # ללא הגדרת מהירות

    assert isinstance(physics, Physics)
    assert physics.get_pos() == (0, 0)

def test_physics_factory_invalid_cfg_key_is_ignored():
    board = Board(cell_H_pix=100, cell_W_pix=100,
                  cell_H_m=1, cell_W_m=1,
                  W_cells=8, H_cells=8,
                  img=None)
    factory = PhysicsFactory(board)
    physics = factory.create((2, 2), {"nonexistent_key": 123})

    assert physics.get_pos() == (2, 2)
