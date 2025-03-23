from game import *
import asyncio

# Inicializar ventana.
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# screen es una superficie (Surface) para renderizar el juego.
# set_mode devuelve un Surface.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Fire Layers")

running = True

game = Game(screen, screen_rect)

async def main():
    # Ciclo principal del juego.
    global running
    while running:
        # Procesar eventos en la fila.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game.hasQuit():
                running = False
            else:
                game.processEvent(event)

        game.run()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())