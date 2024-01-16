import socket
import random


def generate_random_word():
    words = ["apple", "banana", "orange", "grape", "kiwi", "pineapple"]

    return random.choice(words)


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        try:
            while True:
                # Generate a random word
                random_word = generate_random_word()

                # Send the random word to the client
                data = f"{random_word}\n"
                client_socket.sendall(data.encode('utf-8'))

        except ConnectionResetError:
            print("Connection reset by the client")

        finally:
            client_socket.close()


if __name__ == "__main__":
    host = "localhost"
    port = 12345

    start_server(host, port)
