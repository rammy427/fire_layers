from board import *
from typing import Self
from animation import *

class Fighter:
    def __init__(self, brd: Board, grid_pos: pygame.Vector2, team: bool) -> None:
        # Mantener referencia al tablero.
        self.brd = brd
        # Posición inicial del personaje.
        self.grid_pos = grid_pos
        # Cierto si pertenece al jugador 1, falso si pertenece al jugador 2.
        self.team = team
        # Atributos numéricos del personaje.
        self.hp = 10
        self.canAttack = True

        # Cargar animación.
        filename = "sprites/fighter_%s.jpeg" % ("red" if team else "blue")
        self.anim = Animation(32, 3, 0.125, filename)

    def move(self, delta: pygame.Vector2) -> None:
        self.grid_pos += delta
        self.clampToBoard()
        
    def attack(self, target: Self) -> None:
        if self.canAttack:
            target.hp -= 10
            self.canAttack = False
        else:
            print("Se me acabó el turno.")

    def update(self, dt: float) -> None:
        self.anim.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        rect = self.brd.getTileAt(self.grid_pos).rect
        self.anim.draw(rect, screen)

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

    # Función que determina si el personaje ya murió.
    def isDead(self) -> bool:
        return self.hp <= 0