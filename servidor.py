import socket
import threading
import random

# Diccionario para mantener las sesiones de pares
sessions = {}
session_counter = 1

def handle_client(client_socket, client_address):
    global session_counter
    print(f"Nueva conexión desde {client_address}")

    # Asignar el cliente a una sesión
    if len(sessions) % 2 == 0:
        session_id = session_counter
        sessions[session_id] = [client_socket]
        print(f"Esperando al segundo cliente para la sesión {session_id}")
        client_socket.send("Esperando al segundo cliente...".encode())
        session_counter += 1
    else:
        session_id = session_counter - 1
        sessions[session_id].append(client_socket)
        print(f"Sesión {session_id} iniciada con dos clientes")
        
        # Asignar aleatoriamente el primer turno
        first_turn = random.choice([0, 1])
        sessions[session_id][first_turn].send("Sesión iniciada. Es tu turno.".encode())
        sessions[session_id][1 - first_turn].send("Sesión iniciada. Esperando tu turno...".encode())

    # Manejar la comunicación entre los clientes
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Mensaje recibido en la sesión {session_id}: {message}")

            # Enviar el mensaje al otro cliente en la sesión
            if client_socket == sessions[session_id][0]:
                sessions[session_id][1].send(message.encode())
            else:
                sessions[session_id][0].send(message.encode())

            # Si el mensaje es "PASO", indicar que el turno ha terminado
            if message == "PASO":
                if client_socket == sessions[session_id][0]:
                    sessions[session_id][1].send("Es tu turno.".encode())
                else:
                    sessions[session_id][0].send("Es tu turno.".encode())

        except ConnectionResetError:
            print(f"Cliente {client_address} desconectado")
            break

    # Eliminar el cliente de la sesión
    if session_id in sessions:
        if client_socket in sessions[session_id]:
            sessions[session_id].remove(client_socket)
            if not sessions[session_id]:
                del sessions[session_id]
                print(f"Sesión {session_id} cerrada")

    client_socket.close()

# Comienzo de la sesión
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)
    print("Servidor iniciado en localhost:12345")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
