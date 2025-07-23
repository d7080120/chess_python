
from dataclasses import dataclass
from .img import Img

@dataclass
class Board:
    cell_H_pix: int  # גובה התא בפיקסלים
    cell_W_pix: int  # רוחב התא בפיקסלים
    cell_H_m: int    # גובה התא במטרים
    cell_W_m: int    # רוחב התא במטרים
    W_cells: int     # מספר התאים בעמודות
    H_cells: int     # מספר התאים בשורות
    img: Img         # אובייקט התמונה של הלוח

    def clone(self) -> "Board":
        """ מחזיר עותק של הלוח כולל תמונת הלוח. """
        if self.img is None:
            raise ValueError("Board image is None – cannot clone.")
        
        return Board(
            cell_H_pix=self.cell_H_pix,
            cell_W_pix=self.cell_W_pix,
            cell_H_m=self.cell_H_m,
            cell_W_m=self.cell_W_m,
            W_cells=self.W_cells,
            H_cells=self.H_cells,
            img=self.img.copy()  # העתקה אמיתית של תמונת הרקע
        )


    # def get_cell_dimensions(self) -> tuple[int, int]:
    #     """ מחזיר את ממדי התא (גובה ורוחב) בפיקסלים """
    #     return self.cell_H_pix, self.cell_W_pix

    # def get_board_size_in_meters(self) -> tuple[int, int]:
    #     """ מחזיר את ממדי הלוח במטרים (גובה ורוחב) """
    #     return self.cell_H_m * self.H_cells, self.cell_W_m * self.W_cells

    def draw(self, other_img, x, y):
        """ מצייר את הלוח על התמונה """

        self.img.draw_on(other_img, x, y)
