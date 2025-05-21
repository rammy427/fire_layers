from game import *
import socket

# Inicializar ventana.
pygame.init()

DEBUG = True
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FIGHTERS_PER_TEAM = 3

# screen es una superficie (Surface) para renderizar el juego.
# set_mode devuelve un Surface.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Fire Layers")

# Inicializar conexión.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1" if DEBUG else "100.89.70.82"
client_socket.connect((IP, 12345))

running = True
# Booleano para saber si es el turno de ESTE cliente.
has_current_turn = False
# Índice del personaje que se está moviendo.
team_chars = 0

game = Game(screen, screen_rect, FIGHTERS_PER_TEAM)

def processEvent(event: pygame.event.Event):
    global has_current_turn, team_chars
    instruction = ""

    if not game.isOver() and event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_a: instruction = "L"
            case pygame.K_d: instruction = "R"
            case pygame.K_w: instruction = "U"
            case pygame.K_s: instruction = "D"
            case pygame.K_z: instruction = "A"
            case pygame.K_RETURN:
                team_chars = (team_chars + 1) % game.getCurTeamFighterCount()
                if (team_chars == 0):
                    has_current_turn = False
                    game.resetChar()
                    instruction = "P"
                else:
                    instruction = "N"
    
        client_socket.send(instruction.encode())
        # Ejecutar la instrucción para ESTE equipo.
        game.executeAction(instruction, False)

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

        if not has_current_turn:
            # Recibir mensajes del servidor.
            response = client_socket.recv(1024).decode()
            # print(f"Servidor: {response}")

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
                game.resetChar()
                print("Me cedieron el turno!")

            # Ejecutar la instrucción para el OTRO equipo.
            game.executeAction(response, True)

        game.run()

    pygame.quit()

if __name__ == "__main__":
    main()