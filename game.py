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
    def __init__(self, screen: pygame.Surface, screen_rect: pygame.Rect) -> None:
        self.screen = screen
        self.screen_rect = screen_rect
        self.clock = pygame.time.Clock()
        self.state = States.Playing
        # ID de este cliente y el "otro".
        self.this_id = 0
        self.other_id = 1
        self.board = Board(self.screen_rect)
        # Inicializar lista vacía de personajes.
        self.fighters: list[Fighter] = []

    # Función para asignar IDs permanentes de los clientes.
    # Solamente se llama al inicio de la sesión.
    def setIds(self, id: int) -> None:
        self.this_id = id
        self.other_id = 1 - id
        print("This ID: %d\nOther ID: %d" % (self.this_id, self.other_id))

    # Función para generar los personajes fuera del constructor.
    def spawnFighters(self, seed: int) -> None:
        random.seed(seed)
        fighters_per_team = 1
        # Generar personajes.
        # ESTE LO DEBE HACER EL SERVIDOR AL UNIRSE EL CLIENTE 1.
        for n in range(fighters_per_team):
            while True:
                rand_x = random.randint(0, self.board.width // 2 - 2)
                rand_y = random.randint(0, self.board.height - 1)
                if (self.canMove(pygame.Vector2(rand_x, rand_y))):
                    break

            self.fighters.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), True))
        
        # ESTE LO DEBE HACER EL SERVIDOR AL UNIRSE EL CLIENTE 2.
        for n in range(fighters_per_team):
            while True:
                rand_x = random.randint(self.board.width // 2 + 1, self.board.width - 1)
                rand_y = random.randint(0, self.board.height - 1)
                if (self.canMove(pygame.Vector2(rand_x, rand_y))):
                    break

            self.fighters.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), False))

    def executeAction(self, instruction: str, other: bool) -> None:
        id = self.other_id if other else self.this_id
        delta_pos = pygame.Vector2(0, 0)
        match instruction:
            case "L":
                delta_pos = pygame.Vector2(-1, 0)
            case "R":
                delta_pos = pygame.Vector2(1, 0)
            case "U":
                delta_pos = pygame.Vector2(0, -1)
            case "D":
                delta_pos = pygame.Vector2(0, 1)
        
        if delta_pos != pygame.Vector2(0, 0):
            target_pos = self.fighters[id].grid_pos + delta_pos
            if (self.canMove(target_pos)):
                self.fighters[id].move(delta_pos)

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
    
    def canMove(self, target_pos: pygame.Vector2) -> bool:
        for fighter in self.fighters:
            if fighter.grid_pos == target_pos:
                print("¡Está ocupado! :(")
                return False
        return True