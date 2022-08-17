#include <arpa/inet.h>
#include <stdio.h>
#include <string>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>

// CHANGE THESE TO VALUES TO THE ADDRESS OF THE SERVER ////////////
#define PORT 10000
#define ADDRESS "127.0.0.1"
//////////////////////////////////////////////////////////////////

int sendParametersServer(char const* newParameters)
{
    int sock = 0, valread, client_fd;
    struct sockaddr_in serv_addr;
    char buffer[1024] = { 0 };
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }
  
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
  
    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, ADDRESS, &serv_addr.sin_addr)
        <= 0) {
        printf(
            "\n Invalid address/ Address not supported \n");
        return -1;
    }
  
    if ((client_fd
         = connect(sock, (struct sockaddr*)&serv_addr,
                   sizeof(serv_addr)))
        < 0) {
        printf("\n Connection Failed \n");
        return -1;
    }
    send(sock, newParameters, strlen(newParameters), 0);
    printf("\n Message sent \n");
    valread = read(sock, buffer, 1024);

    // closing the connected socket
    close(client_fd);
    return 0;
}
