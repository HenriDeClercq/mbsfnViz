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
    std::string newParameters = std::to_string(SF_ALLOC) + ","  + std::to_string(SF_PERIOD) + std::to_string(60.2);
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
    if (inet_pton(AF_INET, "192.168.112.1", &serv_addr.sin_addr)
        <= 0) {
        printf(
            "\nInvalid address/ Address not supported \n");
        return -1;
    }
  
    if ((client_fd
         = connect(sock, (struct sockaddr*)&serv_addr,
                   sizeof(serv_addr)))
        < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }
    send(sock, newParameters, strlen(newParameters), 0);
    printf("Message sent\n");
    valread = read(sock, buffer, 1024);
    printf("%s\n", buffer);
  
    // closing the connected socket
    close(client_fd);
    return 0;
}

int main() {
    while(1) {
        const char* newParameters = generateParameters();
        sendParametersToServer(newParameters);
        std::this_thread::sleep_for(std::chrono::milliseconds(640));
    }
    return 0;
}