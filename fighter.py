from board import *

class Fighter:
    def __init__(self, brd: Board, grid_pos: pygame.Vector2) -> None:
        # Mantener referencia al tablero.
        self.brd = brd
        # Posición inicial del personaje.
        self.grid_pos = grid_pos
        self.hp = 100

    def draw(self, screen: pygame.Surface) -> None:
        self.brd.getTileAt(self.grid_pos).drawFighter(screen)