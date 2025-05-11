from board import *
from typing import Self

class Fighter:
    def __init__(self, brd: Board, grid_pos: pygame.Vector2, team: bool) -> None:
        # Mantener referencia al tablero.
        self.brd = brd
        # Posición inicial del personaje.
        self.grid_pos = grid_pos
        self.hp = 100
        # Cierto si pertenece al jugador 1, falso si pertenece al jugador 2.
        self.team = team

    def move(self, delta: pygame.Vector2) -> None:
        self.grid_pos += delta
        self.clampToBoard()
        
    def attack(self, target: Self) -> None:
        target.hp -= 10
        print("ATTACKER:\nTeam: %d\nHP: %d" % (self.team, self.hp))
        print("VICTIM:\nTeam: %d\nHP: %d" % (target.team, target.hp))

    def draw(self, screen: pygame.Surface) -> None:
        color = "red" if self.team else "blue"
        self.brd.getTileAt(self.grid_pos).drawFighter(screen, color)

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