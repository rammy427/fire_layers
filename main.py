from game import *
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

game = Game(screen, screen_rect, 0)

def processEvent(event: pygame.event.Event):
    global has_current_turn
    instruction = ""

    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_a: instruction = "L"
            case pygame.K_d: instruction = "R"
            case pygame.K_w: instruction = "U"
            case pygame.K_s: instruction = "D"
            case pygame.K_RETURN:
                has_current_turn = False
                instruction = "P"
    
    client_socket.send(instruction.encode())
    game.executeAction(instruction)

def main():
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

    pygame.quit()

main()