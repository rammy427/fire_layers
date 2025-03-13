from enum import Enum
from animation import *
from board import *

FPS = 60

class States(Enum):
    Playing = 0
    GameOver = 1
    Quit = 2

class Game:
    def __init__(self, screen: pygame.Surface, screen_rect: pygame.Rect) -> None:
        self.screen = screen
        self.screen_rect = screen_rect
        self.clock = pygame.time.Clock()
        self.state = States.Playing
        self.board = Board(self.screen_rect)

    def run(self) -> None:
        # Llenar pantalla con color para "limpiar" el "frame" anterior.
        self.screen.fill("black")
        self.update_frame()
        self.render_frame()
        # Renderizar el nuevo "frame".
        pygame.display.flip()

    def update_frame(self) -> None:
        # Calcular tiempo delta en milisegundos.
        dt = self.clock.tick(FPS) / 1000

    def render_frame(self) -> None:
        self.board.draw(self.screen)

    def resetGame(self) -> None:
        self.state = States.Playing
    
    def endGame(self) -> None:
        self.state = States.GameOver

    def hasQuit(self) -> bool:
        return self.state == States.Quit