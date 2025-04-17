from enum import Enum
from animation import *
from fighter import *
import random

FPS = 60

class States(Enum):
    Playing = 0
    GameOver = 1
    Quit = 2

class Game:
    def __init__(self, screen: pygame.Surface, screen_rect: pygame.Rect, seed: int) -> None:
        self.screen = screen
        self.screen_rect = screen_rect
        self.clock = pygame.time.Clock()
        self.state = States.Playing
        self.board = Board(self.screen_rect)
        # Índice del personaje que se está moviendo.
        self.moving_index = 0
        
        random.seed(seed)
        self.fighters: list[Fighter] = []
        fighters_per_team = 1
        # Generar personajes.
        # ESTE LO DEBE HACER EL SERVIDOR AL UNIRSE EL CLIENTE 1.
        for n in range(fighters_per_team):
            rand_x = random.randint(0, self.board.width // 2 - 2)
            rand_y = random.randint(0, self.board.height - 1)
            self.fighters.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), True))
        
        # ESTE LO DEBE HACER EL SERVIDOR AL UNIRSE EL CLIENTE 2.
        for n in range(fighters_per_team):
            rand_x = random.randint(self.board.width // 2 + 1, self.board.width - 1)
            rand_y = random.randint(0, self.board.height - 1)
            self.fighters.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), False))

    def executeAction(self, instruction: str) -> None:
        match instruction:
            case "L":
                self.fighters[self.moving_index].move((-1, 0))
            case "R":
                self.fighters[self.moving_index].move((1, 0))
            case "U":
                self.fighters[self.moving_index].move((0, -1))
            case "D":
                self.fighters[self.moving_index].move((0, 1))
            case "P":
                self.moving_index = (self.moving_index + 1) % len(self.fighters)

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
        for fighter in self.fighters:
            fighter.draw(self.screen)

    def resetGame(self) -> None:
        self.state = States.Playing
    
    def endGame(self) -> None:
        self.state = States.GameOver

    def hasQuit(self) -> bool:
        return self.state == States.Quit