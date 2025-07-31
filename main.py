"""
main.py - Main entry point for chess game
"""
from src.graphics.img import Img
from src.core.game_logic.Board import Board
from src.core.game_setup.Game import Game
from src.core.game_setup.PieceFactory import PieceFactory
import pathlib
import cv2

def create_chess_game():
    """Create and configure a chess game with the new architecture."""
    print("🎮 Starting Chess Game...")

    # Load the image
    img = Img()
    img_path = pathlib.Path(__file__).parent / "assets" / "images" / "board.png"
    board_pix_size = 800
    cell_size = board_pix_size // 8
    img.read(str(img_path), size=(board_pix_size, board_pix_size))
    
    if img.img is None:
        print("❌ Failed to load board image!")
        return None

    board = Board(
        cell_W_pix=cell_size,
        cell_H_pix=cell_size,
        cell_H_m=1,
        cell_W_m=1,
        W_cells=8,
        H_cells=8,
        img=img
    )

    pieces_root = pathlib.Path(__file__).parent / "assets" / "pieces"
    factory = PieceFactory(board, pieces_root)

    start_positions = [
        ("RB", (0, 0)), ("NB", (1, 0)), ("BB", (2, 0)), ("QB", (3, 0)), 
        ("KB", (4, 0)), ("BB", (5, 0)), ("NB", (6, 0)), ("RB", (7, 0)),
        ("PB", (0, 1)), ("PB", (1, 1)), ("PB", (2, 1)), ("PB", (3, 1)), 
        ("PB", (4, 1)), ("PB", (5, 1)), ("PB", (6, 1)), ("PB", (7, 1)),
        ("PW", (0, 6)), ("PW", (1, 6)), ("PW", (2, 6)), ("PW", (3, 6)), 
        ("PW", (4, 6)), ("PW", (5, 6)), ("PW", (6, 6)), ("PW", (7, 6)),
        ("RW", (0, 7)), ("NW", (1, 7)), ("BW", (2, 7)), ("QW", (3, 7)), 
        ("KW", (4, 7)), ("BW", (5, 7)), ("NW", (6, 7)), ("RW", (7, 7)),
    ]

    pieces = []
    piece_counters = {}

    for p_type, cell in start_positions:
        try:
            if p_type not in piece_counters:
                piece_counters[p_type] = 0
            piece_id = f"{p_type}{piece_counters[p_type]}"
            piece_counters[p_type] += 1

            piece = factory.create_piece(p_type, cell, None)
            piece.piece_id = piece_id
            if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
                piece._state._physics.piece_id = piece_id
            pieces.append(piece)
            
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    from src.ui.PlayerNameManager import PlayerNameManager
    from src.ui.window_settings import PLAYER_DIALOG_POSITION
    
    temp_name_manager = PlayerNameManager()
    temp_name_manager.get_player_names(window_position=PLAYER_DIALOG_POSITION)
    
    game = Game(pieces, board)
    
    for piece in pieces:
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            piece._state._physics.user_input_queue = game.user_input_queue
            piece._state._game_queue = game.game_queue
    
    game.player_name_manager.player1_name = temp_name_manager.player1_name
    game.player_name_manager.player2_name = temp_name_manager.player2_name
    
    game.pieces = pieces
    
    print("\n🎯 Game Controls:")
    print("   Player 1 (White): 8=up, 2=down, 4=left, 6=right, 5/0/Enter=select")
    print("   Player 2 (Black): W=up, S=down, A=left, D=right, Space=select")
    print("   ESC or Q: Exit game\n")
    
    return game


def demonstrate_architecture():
    """Demonstrate the benefits of the new architecture."""
    pass


if __name__ == "__main__":
    try:
        demonstrate_architecture()
        
        game = create_chess_game()
        if game:
            game.run()
        else:
            print("❌ Failed to create game!")
            
    except KeyboardInterrupt:
        print("\n👋 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("\n🎮 Thank you for playing!")
