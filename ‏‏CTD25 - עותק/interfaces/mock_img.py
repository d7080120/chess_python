# mock_img.py
from .img import Img


class MockImg(Img):
    """Headless Img that just records calls."""
    traj: list[tuple[int, int]] = []  # every draw_on() position
    txt_traj: list[tuple[tuple[int, int], str]] = []

    def __init__(self):  # override, no cv2 needed
        self.img = "MOCK-PIXELS"

    def read(self, path, *_, **__):
        self.W = self.H = 1
        return self  # chain-call compatible

    def draw_on(self, other, x, y):
        MockImg.traj.append((x, y))

    def put_text(self, txt, x, y, font_size, *_, **__):
        MockImg.txt_traj.append(((x, y), txt))

    def show(self):
        pass  # do nothing

    # הוספת המתודה copy() למחלקת MockImg
    def copy(self):
        new_mock_img = MockImg()
        # העתקת ערכים במקום שיתוף רפרנס
        new_mock_img.img = self.img if isinstance(self.img, str) else self.img.copy()
        new_mock_img.W = getattr(self, "W", None)
        new_mock_img.H = getattr(self, "H", None)
        return new_mock_img
    # helper for tests
    @classmethod
    def reset(cls):
        cls.traj.clear()
        cls.txt_traj.clear()
