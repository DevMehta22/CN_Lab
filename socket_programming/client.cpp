#include <cstring>
#include <iostream>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

using namespace std;

int main() {
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        cerr << "Error creating socket." << endl;
        return -1;
    }

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8080);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    int connectionStatus = connect(clientSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress));
    if (connectionStatus == -1) {
        cerr << "Unable to connect to server. The server might have rejected the connection or is unavailable." << endl;
        close(clientSocket);
        return -1;
    }

    cout << "Waiting for server confirmation..." << endl;

    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));

    int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
    if (bytesReceived == -1) {
        cerr << "Error receiving server confirmation." << endl;
        close(clientSocket);
        return -1;
    }

    string serverResponse(buffer);
    if (serverResponse == "accepted") {
        cout << "Connection accepted by the server. You can now send messages." << endl;
    } else {
        cout << "Connection rejected by the server." << endl;
        close(clientSocket);
        return 0;
    }

    string message;
    while (true) {
        cout << "Enter message (type 'exit' to quit): ";
        getline(cin, message);

        if (message == "exit") {
            break; 
        }

        send(clientSocket, message.c_str(), message.size(), 0);

        memset(buffer, 0, sizeof(buffer));

        bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived > 0) {
            cout << "Response from server: " << buffer << endl;
        } else if (bytesReceived == 0) {
            cout << "Server closed the connection." << endl;
            break;
        } else {
            cerr << "Error receiving response from server." << endl;
            break;
        }
    }

    close(clientSocket);
    return 0;
}
