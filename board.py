import pygame

TILE_SIZE = 32

# Tablero es un arreglo de fichas.
class Board:

    # Definición para objeto que representa una ficha del tablero.
    class Tile:
        def __init__(self, pos) -> None:
            self.rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
            self.color = pygame.Color("yellow")
            self.padding = 5

        def draw(self, screen: pygame.Surface):
            pygame.draw.rect(screen, self.color, self.rect.inflate(-self.padding, -self.padding))

    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.rows = 20
        self.columns = 20

        # Calcular posición para centralizar el tablero.
        top_left = screen_rect.center - TILE_SIZE / 2 * pygame.Vector2(self.rows, self.columns)
        
        self.tiles = []
        # Generar fichas del tablero.
        for row in range(self.rows):
            for col in range(self.columns):
                self.tiles.append(self.Tile(top_left + TILE_SIZE * pygame.Vector2(row, col)))
    
    def draw(self, screen: pygame.Surface) -> None:
        for tile in self.tiles:
            tile.draw(screen)