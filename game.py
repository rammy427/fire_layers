from enum import Enum
from animation import *
from fighter import *
from text import *
import random

FPS = 60

class States(Enum):
    Playing = 0
    GameOver = 1
    Quit = 2
    Waiting = 3

class Game:
    def __init__(self, screen: pygame.Surface, screen_rect: pygame.Rect, fighters_per_team: int) -> None:
        self.screen = screen
        self.screen_rect = screen_rect
        self.clock = pygame.time.Clock()
        self.text_manager = TextManager(screen_rect)
        self.state = States.Waiting
        # ID de este cliente y el "otro".
        self.this_id = 0
        self.other_id = 1
        self.board = Board(self.screen_rect)
        # Manejar personajes de los jugadores.
        self.fighters: list[list[Fighter]] = []
        self.fighters_per_team = fighters_per_team
        # Índice del personaje que se está moviendo.
        self.cur_char = 0
        # Equipo ganador.
        self.winner = -1

    # Función para asignar IDs permanentes de los clientes.
    # Solamente se llama al inicio de la sesión.
    def setIds(self, id: int) -> None:
        self.this_id = id
        self.other_id = 1 - id
        print("This ID: %d\nOther ID: %d" % (self.this_id, self.other_id))

    # Función para generar los personajes fuera del constructor.
    def spawnFighters(self, seed: int) -> None:
        random.seed(seed)
        # Generar personajes del primer equipo.
        first_team: list[Fighter] = []
        for n in range(self.fighters_per_team):
            while True:
                rand_x = random.randint(0, BOARD_WIDTH // 2 - 2)
                rand_y = random.randint(0, BOARD_HEIGHT - 1)
                if (self.canMove(pygame.Vector2(rand_x, rand_y))):
                    break

            first_team.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), True, seed + n))
        
        # Generar personajes del segundo equipo.
        second_team: list[Fighter] = []
        for n in range(self.fighters_per_team):
            while True:
                rand_x = random.randint(BOARD_WIDTH // 2 + 1, BOARD_HEIGHT - 1)
                rand_y = random.randint(0, BOARD_HEIGHT - 1)
                if (self.canMove(pygame.Vector2(rand_x, rand_y))):
                    break

            second_team.append(Fighter(self.board, pygame.Vector2(rand_x, rand_y), False, seed + n + 3))
        
        # "Concatenar" ambos equipos.
        self.fighters.append(first_team)
        self.fighters.append(second_team)

        # Comenzar el juego.
        self.state = States.Playing

    def executeAction(self, instruction: str, other: bool) -> None:
        team_index = self.other_id if other else self.this_id
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
            case "A":
                self.executeAttack(team_index)
            case "N":
                self.fighters[team_index][self.cur_char].canAttack = True
                self.cur_char += 1
            case "P":
                self.fighters[team_index][self.cur_char].canAttack = True
        
        if delta_pos != pygame.Vector2(0, 0):
            target_pos = self.fighters[team_index][self.cur_char].grid_pos + delta_pos
            if (self.canMove(target_pos)):
                self.fighters[team_index][self.cur_char].move(delta_pos)

    def executeAttack(self, cur_team: int) -> None:
        other_team = 1 - cur_team
        src_pos = self.fighters[cur_team][self.cur_char].grid_pos
        up = src_pos - pygame.Vector2(0, 1)
        down = src_pos + pygame.Vector2(0, 1)
        left = src_pos - pygame.Vector2(1, 0)
        right = src_pos + pygame.Vector2(1, 0)

        target_index = -1
        # Buscar el primer soldado del otro equipo que sea adyacente.
        for i in range(len(self.fighters[other_team])):
            target_pos = self.fighters[other_team][i].grid_pos
            if target_pos in (up, down, left, right):
                target_index = i
                break

        if target_index == -1:
            print("¡No hay soldados cerca! No puedo atacar.")
        else:
            attacker = self.fighters[cur_team][self.cur_char]
            victim = self.fighters[other_team][target_index]
            attacker.attack(victim)

        self.killFighters()

    # Cada jugador muerto se elimina de la lista.
    def killFighters(self) -> None:
        if self.fighters:
            self.fighters[self.this_id] = [fighter for fighter in self.fighters[self.this_id] if not fighter.isDead()]
            self.fighters[self.other_id] = [fighter for fighter in self.fighters[self.other_id] if not fighter.isDead()]

        # Si todos los soldados de un equipo ya murieron, decidir ganador.
        if not self.fighters[self.this_id]:
            self.winner = self.other_id
            self.endGame()
        elif not self.fighters[self.other_id]:
            self.winner = self.this_id
            self.endGame()

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
        for team in self.fighters:
            for fighter in team:
                fighter.update(dt)

    def render_frame(self) -> None:
        self.board.draw(self.screen)
        if self.state == States.Playing:
            self.text_manager.drawControls(self.screen)
            self.text_manager.drawTeamInfo(self.fighters, self.screen)
            for team in self.fighters:
                for fighter in team:
                    fighter.draw(self.screen)
        elif self.state == States.GameOver:
            self.text_manager.drawGameOver(self.winner == self.this_id, self.screen)

    def resetFighters(self) -> None:
        self.cur_char = 0
        for team in self.fighters:
            for fighter in team:
                fighter.canAttack = True

    def resetGame(self) -> None:
        self.state = States.Playing
    
    def endGame(self) -> None:
        self.state = States.GameOver

    def isOver(self) -> bool:
        return self.state == States.GameOver

    def hasQuit(self) -> bool:
        return self.state == States.Quit
    
    def canMove(self, target_pos: pygame.Vector2) -> bool:
        for team in self.fighters:
            for fighter in team:
                if fighter.grid_pos == target_pos:
                    print("¡Está ocupado! :(")
                    return False
        return True
    
    def getCurTeamFighterCount(self) -> int:
        return len(self.fighters[self.this_id])