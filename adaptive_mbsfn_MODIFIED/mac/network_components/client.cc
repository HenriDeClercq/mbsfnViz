#include <arpa/inet.h>
#include <stdio.h>
#include <string>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 10000


#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>

const char* generateParameters(){ 
    // Declarations   
    const std::vector<int>  legal_SF_ALLOC = {1,2,3,4,5,6};
    const std::vector<int>  legal_SF_PERIOD = {1,2,4,8,16,32};
    std::random_device random_ALLOC; 
    std::random_device random_PERIOD;
    std::mt19937 eng_ALLOC(random_ALLOC());
    std::mt19937 eng_PERIOD(random_PERIOD());
    std::uniform_int_distribution<> distr_ALLOC(0, legal_SF_ALLOC.size() - 1);
    std::uniform_int_distribution<> distr_PERIOD(0, legal_SF_PERIOD.size() - 1);

    //Generate new parameters
    int SF_ALLOC = legal_SF_ALLOC[distr_ALLOC(eng_ALLOC)];
    int SF_PERIOD = legal_SF_PERIOD[distr_PERIOD(eng_PERIOD)];
    std::string newParameters = std::to_string(SF_ALLOC) + ","  + std::to_string(SF_PERIOD);
    return newParameters.c_str();
    }

int sendParametersToServer(char const* newParameters)
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
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)
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

void runClient() {
    while(1) {
        const char* newParameters = generateParameters();
        sendParametersToServer(newParameters);
    }
}
