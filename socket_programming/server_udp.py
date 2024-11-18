import socket

PORT = 8080
BUFFER_SIZE = 1024

def main():
    try:
        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print(f"Socket creation failed: {e}")
        return

    server_address = ('', PORT)  # Bind to all available interfaces, port 8080

    try:
        # Bind the socket to the address
        server_socket.bind(server_address)
        print(f"UDP server listening on port {PORT}...")
    except socket.error as e:
        print(f"Bind failed: {e}")
        server_socket.close()
        return

    try:
        while True:
            # Receive message from the client
            message, client_address = server_socket.recvfrom(BUFFER_SIZE)
            print(f"Message from client: {message.decode('utf-8')}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        server_socket.close()

if __name__ == "__main__":
    main()