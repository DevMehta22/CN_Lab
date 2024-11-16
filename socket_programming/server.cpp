#include<iostream>
#include<vector>
#include<sys/socket.h>
#include<netinet/in.h>
#include<cstring>
#include<unistd.h>

using namespace std;

int main(){
    int serverSocket = socket(AF_INET,SOCK_STREAM,0);
    if (serverSocket == -1) {
        cerr << "Failed to create socket" << endl;
        return -1;
    }

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8080);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));
    if (listen(serverSocket, 5) == -1) {
        cerr << "Error in listening" << endl;
        return -1;
    }
    
    cout << "Server is listening on port 8080" << endl;

    while (true) {
        int clientSocket = accept(serverSocket, nullptr, nullptr);
        if (clientSocket == -1) {
            cerr << "Error accepting client" << endl;
            continue;
        }

        char choice;
        cout << "Incoming connection request. Do you want to accept? (y/n): ";
        cin >> choice;

        if (choice == 'y' || choice == 'Y') {
            cout << "Connection accepted from client" << endl;
            send(clientSocket, "accepted", strlen("accepted"), 0);
        } else {
            cout << "Connection rejected. Closing client socket..." << endl;
            send(clientSocket, "rejected", strlen("rejected"), 0);
            close(clientSocket);  
            continue; 
        }

        char buffer[1024];
        while (true) {
            memset(buffer, 0, sizeof(buffer));
            int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
            if (bytesReceived == -1) {
                cout << "Error in receiving data" << endl;
                break;
            } else if (bytesReceived == 0) {
                cout << "Client disconnected" << endl;
                break;
            }
            cout << "Message from client: " << buffer << endl;

            string response = "Message received: " + string(buffer);
            send(clientSocket, response.c_str(), response.size(), 0);
        }

        close(clientSocket);
    }

    close(serverSocket);
    return 0;
}
