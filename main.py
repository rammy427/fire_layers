from game import *
import asyncio
import socket

# Inicializar ventana.
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# screen es una superficie (Surface) para renderizar el juego.
# set_mode devuelve un Surface.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Fire Layers")

# Inicializar conexión.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

running = True
# Booleano para saber si es el turno de ESTE cliente.
has_current_turn = False

game = Game(screen, screen_rect)

def processEvent(event: pygame.event.Event):
    global has_current_turn
    if event.type == pygame.KEYDOWN:
        # Movida a la izquierda.
        if event.key in (pygame.K_a, pygame.K_LEFT):
            client_socket.send("LEFT".encode())
            game.executeAction("LEFT")

        # Movida a la derecha.
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            client_socket.send("RIGHT".encode())
            game.executeAction("RIGHT")

        # Movida hacia arriba.
        elif event.key in (pygame.K_w, pygame.K_UP):
            client_socket.send("UP".encode())
            game.executeAction("UP")

        # Movida hacia abajo.
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            client_socket.send("DOWN".encode())
            game.executeAction("DOWN")

        # Cambio de turno.
        elif event.key == pygame.K_RETURN:
            has_current_turn = False
            client_socket.send("PASO".encode())
            game.executeAction("PASO")

async def main():
    # Ciclo principal del juego.
    global running, has_current_turn
    while running:
        # Procesar eventos en la fila.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game.hasQuit():
                running = False
            elif has_current_turn:
                processEvent(event)
            else:
                # Recibir mensajes del servidor.
                response = client_socket.recv(1024).decode()
                print(f"Servidor: {response}")
                if "Es tu turno" in response:
                    has_current_turn = True
                    print("Me cedieron el turno!")

        game.run()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())