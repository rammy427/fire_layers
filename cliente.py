import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    while True:
        # Recibir mensajes del servidor
        response = client_socket.recv(1024).decode()
        print(f"Servidor: {response}")

        # Enviar mensajes al servidor solo si es tu turno
        if "Es tu turno" in response:
            while True:
                message = input("Escribe tu mensaje (o 'PASO' para terminar tu turno): ")
                client_socket.send(message.encode())

                if message == "PASO":
                    print("Turno terminado. Esperando tu próximo turno...")
                    break


if __name__ == "__main__":
    client()