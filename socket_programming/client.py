import socket

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error creating socket: {e}")
        return

    server_address = ('127.0.0.1', 8080)  # Server IP and Port

    try:
        client_socket.connect(server_address)
    except socket.error as e:
        print(f"Unable to connect to server: {e}")
        client_socket.close()
        return

    print("Waiting for server confirmation...")

    try:
        buffer = client_socket.recv(1024).decode('utf-8')
        if buffer == "accepted":
            print("Connection accepted by the server. You can now send messages.")
        else:
            print("Connection rejected by the server.")
            client_socket.close()
            return
    except socket.error as e:
        print(f"Error receiving server confirmation: {e}")
        client_socket.close()
        return

    try:
        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == "exit":
                break

            client_socket.sendall(message.encode('utf-8'))

            buffer = client_socket.recv(1024).decode('utf-8')
            if buffer:
                print(f"Response from server: {buffer}")
            else:
                print("Server closed the connection.")
                break
    except socket.error as e:
        print(f"Error during communication: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()