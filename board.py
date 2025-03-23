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

        def draw(self, screen: pygame.Surface) -> None:
            pygame.draw.rect(screen, self.color, self.rect.inflate(-self.padding, -self.padding))

        def drawFighter(self, screen: pygame.Surface, color: pygame.Color) -> None:
            pygame.draw.circle(screen, color, self.rect.center, TILE_SIZE // 2)

    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.width = 20
        self.height = 20

        # Calcular posición para centralizar el tablero.
        top_left = screen_rect.center - TILE_SIZE / 2 * pygame.Vector2(self.width, self.height)
        
        self.tiles = []
        # Generar fichas del tablero.
        for y in range(self.width):
            for x in range(self.height):
                self.tiles.append(self.Tile(top_left + TILE_SIZE * pygame.Vector2(x, y)))
    
    def draw(self, screen: pygame.Surface) -> None:
        for tile in self.tiles:
            tile.draw(screen)

    def getTileAt(self, grid_pos: pygame.Vector2) -> Tile:
        return self.tiles[int(grid_pos.y * self.height + grid_pos.x)]