import pygame

TILE_SIZE = 32
TILE_PADDING = 5
BOARD_WIDTH = 14
BOARD_HEIGHT = 14

# Tablero es un arreglo de fichas.
class Board:

    # Definición para objeto que representa una ficha del tablero.
    class Tile:
        def __init__(self, pos) -> None:
            self.rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
            self.color = pygame.Color("#80a080")

        def draw(self, screen: pygame.Surface) -> None:
            pygame.draw.rect(screen, self.color, self.rect)

        def drawFighter(self, screen: pygame.Surface, color: pygame.Color) -> None:
            pygame.draw.circle(screen, color, self.rect.center, TILE_SIZE // 2)

    def __init__(self, screen_rect: pygame.Rect) -> None:
        # Calcular posición para centralizar el tablero.
        top_left = screen_rect.center - (TILE_SIZE + TILE_PADDING) / 2 * pygame.Vector2(BOARD_WIDTH, BOARD_HEIGHT)
        top_left.y -= TILE_SIZE
        
        self.tiles = []
        # Generar fichas del tablero.
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.tiles.append(self.Tile(top_left + (TILE_SIZE + TILE_PADDING) * pygame.Vector2(x, y)))
    
    def draw(self, screen: pygame.Surface) -> None:
        for tile in self.tiles:
            tile.draw(screen)

    def getTileAt(self, grid_pos: pygame.Vector2) -> Tile:
        return self.tiles[int(grid_pos.y * BOARD_WIDTH + grid_pos.x)]