import pathlib
from interfaces.Moves import Moves

def test_moves_loading():
    path = pathlib.Path("CTD25/pieces/RB/moves.txt")
    moves = Moves(path, dims=(8, 8))
    assert len(moves.deltas) > 0
    assert (1, 0) in moves.deltas
    assert (0, -7) in moves.deltas

def test_moves_from_center():
    path = pathlib.Path("CTD25/pieces/RB/moves.txt")
    moves = Moves(path, dims=(8, 8))
    result = moves.get_moves(4, 4)

    # ודא שכולם בגבולות
    for r2, c2 in result:
        assert 0 <= r2 < 8
        assert 0 <= c2 < 8

    # בדוק שנמצאים מהלכים אופקיים ואנכיים בסיסיים
    assert (5, 4) in result
    assert (3, 4) in result
    assert (4, 5) in result
    assert (4, 3) in result


def test_moves_from_edge():
    path = pathlib.Path("CTD25/pieces/RB/moves.txt")
    moves = Moves(path, dims=(8, 8))
    result = moves.get_moves(0, 0)
    # חלק מהמהלכים מחוץ ללוח ולכן לא חוקיים
    assert (1, 0) in result
    assert (0, 1) in result
    assert (-1, 0) not in result
    assert (0, -1) not in result
    assert len(result) < len(moves.deltas)

def test_moves_bounds_check():
    path = pathlib.Path("CTD25/pieces/RB/moves.txt")
    moves = Moves(path, dims=(8, 8))
    for r in range(8):
        for c in range(8):
            for nr, nc in moves.get_moves(r, c):
                assert 0 <= nr < 8
                assert 0 <= nc < 8
