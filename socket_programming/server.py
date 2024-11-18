import socket

def main():
    try:
        # Create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Failed to create socket: {e}")
        return

    server_address = ('0.0.0.0', 8080)  # Listen on all available interfaces, port 8080

    try:
        # Bind the socket to the address
        server_socket.bind(server_address)
        # Listen for incoming connections
        server_socket.listen(5)
        print("Server is listening on port 8080...")
    except socket.error as e:
        print(f"Error in binding or listening: {e}")
        server_socket.close()
        return

    while True:
        try:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Incoming connection request from {client_address}")

            # Prompt server operator for connection approval
            choice = input("Do you want to accept the connection? (y/n): ").strip().lower()
            if choice == 'y':
                print("Connection accepted.")
                client_socket.sendall(b"accepted")
            else:
                print("Connection rejected. Closing client socket...")
                client_socket.sendall(b"rejected")
                client_socket.close()
                continue

            # Communication loop with the client
            while True:
                buffer = client_socket.recv(1024).decode('utf-8')
                if not buffer:
                    print("Client disconnected.")
                    break
                print(f"Message from client: {buffer}")

                response = f"Message received: {buffer}"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error during communication: {e}")
        finally:
            # Close the client socket
            client_socket.close()
            server_socket.close()

if __name__ == "__main__":
    main()