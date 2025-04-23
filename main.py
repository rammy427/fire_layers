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
DEBUG = True
IP = "127.0.0.1" if DEBUG else "100.89.70.82"
client_socket.connect((IP, 12345))

running = True
# Booleano para saber si es el turno de ESTE cliente.
has_current_turn = False

game = Game(screen, screen_rect)

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

                client_id = 0
                # Calcular ID del cliente la primera vez que se recibe el mensaje.
                if "Sesión iniciada" in response:
                    client_id = int("Es tu turno" in response)
                    game.setIds(client_id)

                if "SEMILLA" in response:
                    # Analizando string con la semilla.
                    seed = int(response.split(':')[1][:2])
                    print(seed)
                    # Generando posiciones de los soldados con la semilla.
                    game.spawnFighters(seed)

                if "Es tu turno" in response:
                    has_current_turn = True
                    print("Me cedieron el turno!")

        game.run()

    pygame.quit()

if __name__ == "__main__":
    main()