import socket

PORT = 8080
SERVER_ADDRESS = "127.0.0.1"  # Change this to the server's IP address if needed

def main():
    try:
        # Create a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print(f"Socket creation failed: {e}")
        return

    server_address = (SERVER_ADDRESS, PORT)

    try:
        while True:
            # Get user input
            message = input("Enter message to send (type 'exit' to quit): ")

            if message.lower() == "exit":
                print("Exiting...")
                break

            # Send the message to the server
            client_socket.sendto(message.encode('utf-8'), server_address)
            print("Message sent to server")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    main()