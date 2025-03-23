from board import *

class Fighter:
    def __init__(self, brd: Board, grid_pos: pygame.Vector2) -> None:
        # Mantener referencia al tablero.
        self.brd = brd
        # Posición inicial del personaje.
        self.grid_pos = grid_pos
        self.hp = 100

    def move(self, delta: pygame.Vector2) -> None:
        self.grid_pos += delta
        self.clampToBoard()

    def draw(self, screen: pygame.Surface) -> None:
        self.brd.getTileAt(self.grid_pos).drawFighter(screen)

    # Atrapar personaje en el tablero.
    def clampToBoard(self) -> None:
        if self.grid_pos.x < 0:
            self.grid_pos.x = 0
        elif self.grid_pos.x >= self.brd.width:
            self.grid_pos.x = self.brd.width - 1

        if self.grid_pos.y < 0:
            self.grid_pos.y = 0
        elif self.grid_pos.y >= self.brd.height:
            self.grid_pos.y = self.brd.height - 1